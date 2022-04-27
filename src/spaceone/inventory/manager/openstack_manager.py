import time
import logging
import json
import openstack
import copy
from spaceone.core.manager import BaseManager
from spaceone.inventory.manager.resources.compute import InstanceResource
from spaceone.inventory.manager.resources.compute import FlavorResource
from spaceone.inventory.manager.resources.block_storage import VolumeResource
from spaceone.inventory.manager.resources.network import NetworkResource
from spaceone.inventory.manager.resources.resource import BaseResource
from spaceone.inventory.model.common.response import CloudServiceResponse
from spaceone.inventory.model.common.response import CloudServiceTypeResourceResponse
from spaceone.inventory.model.common.base import CloudServiceResource
from spaceone.inventory.model.common.base import CloudServiceReferenceModel
from spaceone.inventory.model.resources.base import ResourceModel
from openstack.connection import Connection
from spaceone.inventory.error.base import CollectorError

from typing import (

    List,
    Dict,
    Optional,
    Union,
    Tuple,
    Callable,
    Iterator
)

_LOGGER = logging.getLogger(__name__)

__all__ = ['OpenstackManager']


class OpenstackManager(BaseManager):

    _resource_cls_list: List[Callable[[Optional[Connection]], 'BaseResource']] = [InstanceResource, VolumeResource,
                                                                                  NetworkResource]
    _resource_obj_list: List[BaseResource] = []
    _secret_data: Dict = {}
    __conn: Optional[Connection] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._resource_obj_list = []
        self._secret_data = {}
        self.__conn = None

    @property
    def conn(self) -> Connection:
        return self.__conn

    @conn.setter
    def conn(self, conn: Connection = None) -> None:
        self.__conn = conn

    @property
    def project_id(self) -> str:
        return self._secret_data.get('project_id')

    @property
    def account(self) -> str:
        return self._secret_data.get('username')

    @property
    def region_code(self) -> str:
        return self._secret_data.get('region_name')

    def _set_connection(self, secret_data: Optional[Dict] = {}) -> None:

        # Initialize and turn on debug logging

        openstack.enable_logging(debug=False)

        if secret_data is None:
            raise CollectorError(message='The secret data must exist for connection.')

        try:

            required_keys = ['username', 'password', 'user_domain_name', 'auth_url', 'project_id',
                             'identity_api_version', 'interface', 'region_name']

            for key in required_keys:
                if key not in secret_data.keys() or not (secret_data[key] and secret_data[key].strip()):
                    raise CollectorError(message=f"Invalid input for field {required_keys}")

            username = secret_data.get('username')
            password = secret_data.get('password')
            user_domain_name = secret_data.get('user_domain_name')
            auth_url = secret_data.get('auth_url')
            project_id = secret_data.get('project_id')
            identity_api_version = secret_data.get('identity_api_version')
            interface = secret_data.get('interface')
            region_name = secret_data.get('region_name')  # This is used as region_code

            # Initialize connection
            self._secret_data = copy.deepcopy(secret_data)
            self.conn = openstack.connection.Connection(
                region_name=region_name,
                auth=dict(
                    auth_url=auth_url,
                    username=username,
                    password=password,
                    project_id=project_id,
                    user_domain_name=user_domain_name),
                identity_api_version=identity_api_version,
                interface=interface)

        except Exception as e:
            raise CollectorError(message='Creating openstack connection failed', cause=e)

    def _create_resource_objs(self, filter_params: Dict = None) -> None:

        filters = []

        if 'cloud_service_types' in filter_params and isinstance(filter_params.get('cloud_service_types'), list):
            filters = filter_params.get('cloud_service_types')

        _LOGGER.debug(f"Filter List : {filters}")

        # Add resources object type for collecting
        _LOGGER.debug(f"Total resource class list : {self._resource_cls_list}")
        for resource_cls in self._resource_cls_list:
            resource_obj = resource_cls(self.conn)

            if len(filters) == 0 or resource_obj.cloud_service_type_name in filters:
                self._resource_obj_list.append(resource_obj)
                _LOGGER.debug(f"Resource Added : {resource_obj.cloud_service_type_name}")

    def _collect_objs_resources(self) -> Iterator[List[ResourceModel]]:

        for resource_obj in self._resource_obj_list:
            yield resource_obj.collect()

    def _create_cloud_service_responses(self, collected_resources: List[Tuple[ResourceModel, BaseResource]]) \
            -> Iterator[CloudServiceResponse]:

        for collected_resource_model, resource_obj in collected_resources:
            resource = CloudServiceResource({'data': collected_resource_model,
                                             'account': self.project_id,
                                             'reference': CloudServiceReferenceModel({"resource_id": collected_resource_model.id}),
                                             'region_code': self.region_code,
                                             '_metadata': resource_obj.cloud_service_meta,
                                             'cloud_service_group': resource_obj.cloud_service_group_name,
                                             'cloud_service_type': resource_obj.cloud_service_type_name})
            _LOGGER.debug(resource.to_primitive())
            yield CloudServiceResponse({'resource': resource})

    def _create_cloud_service_type_response(self, resource_obj: BaseResource) -> CloudServiceTypeResourceResponse:
        cst_response = CloudServiceTypeResourceResponse({"resource": resource_obj.cloud_service_type_resource})
        _LOGGER.debug(cst_response.to_primitive())
        return cst_response

    def collect_resources(self, params: Dict) -> Union[Iterator[CloudServiceResponse],
                                                       Iterator[CloudServiceTypeResourceResponse]]:

        if 'secret_data' not in params:
            raise CollectorError(message='secret_data key must exist in params')

        self._set_connection(params.get('secret_data'))

        filter_params = params.get('filter')

        self._create_resource_objs(filter_params)

        for resource_obj in self._resource_obj_list:
            cloud_svc_type_response = self._create_cloud_service_type_response(resource_obj)
            yield cloud_svc_type_response

        for collected_obj_resources in self._collect_objs_resources():
            yield from self._create_cloud_service_responses(collected_obj_resources)
