import time
import logging
import json
import openstack

from spaceone.core.manager import BaseManager
from spaceone.inventory.manager.resources.compute import InstanceResource
from spaceone.inventory.manager.resources.compute import FlavorResource
from spaceone.inventory.manager.resources.block_storage import VolumeResource
from spaceone.inventory.manager.resources.network import NetworkResource
from spaceone.inventory.manager.resources.resource import BaseResource
from spaceone.inventory.model.common.response import CloudServiceResponse
from spaceone.inventory.model.common.response import CloudServiceTypeResourceResponse
from spaceone.inventory.model.common.base import CloudServiceResource
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
    _resource_obj_list: List[BaseResource] = []
    """
    _resource_cls_list: List[Callable[[Optional[Connection]], 'BaseResource']] = [InstanceResource, VolumeResource,
                                                                                  NetworkResource, FlavorResource]
    """
    _resource_cls_list: List[Callable[[Optional[Connection]], 'BaseResource']] = [InstanceResource, VolumeResource,
                                                                                  NetworkResource]

    _secret_data: Dict = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__conn = None

    @property
    def conn(self) -> Connection:
        return self.__conn

    @conn.setter
    def conn(self, conn: Connection = None) -> None:
        self.__conn = conn

    def _set_connection(self, secret_data: Optional[Dict] = {}) -> None:

        # Initialize and turn on debug logging

        openstack.enable_logging(debug=False)

        if secret_data is None:
            raise CollectorError(message='The secret data must exist for connection.')

        try:

            required_keys = ['username', 'password', 'user_domain_name', 'auth_url', 'project_id',
                             'identity_api_version', 'interface', 'region_name']

            for key in required_keys:
                if key not in secret_data.keys() or not(secret_data[key] and secret_data[key].strip()):
                    raise CollectorError(message=f"Invalid input for field {required_keys}")

            username = secret_data.get('username')
            password = secret_data.get('password')
            user_domain_name = secret_data.get('user_domain_name')
            auth_url = secret_data.get('auth_url')
            project_id = secret_data.get('project_id')
            identity_api_version = secret_data.get('identity_api_version')
            interface = secret_data.get('interface')
            region_name = secret_data.get('region_name')

            # Initialize connection
            self.secret_data = secret_data
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

    def _create_resource_objs(self, options: Dict = None) -> None:

        # to do
        # resource filtering with options if you want
        # Add resources object type for collecting
        for resource_cls in self._resource_cls_list:
            resource_obj = resource_cls(self.conn)
            self._resource_obj_list.append(resource_obj)

    def _collect_objs_resources(self) -> Iterator[List[ResourceModel]]:

        for resource_obj in self._resource_obj_list:
            yield resource_obj.collect()

    def _create_cloud_sevice_responses(self, collected_resources: List[Tuple[ResourceModel, BaseResource]]) \
            -> Iterator[CloudServiceResponse]:

        for collected_resource_model, resource_obj in collected_resources:
            resource = CloudServiceResource({'data': collected_resource_model,
                                             'account': self.secret_data.get('username'),
                                             'project_id': self.secret_data.get('project_id'),
                                             '_metadata': resource_obj.cloud_service_meta,
                                             'cloud_service_group': resource_obj.cloud_service_type_name,
                                             'cloud_service_type': resource_obj.cloud_service_type_name})

            yield CloudServiceResponse({'resource': resource})

    def _create_cloud_sevice_type_response(self, resource_obj: BaseResource) -> CloudServiceTypeResourceResponse:
        return CloudServiceTypeResourceResponse({"resource": resource_obj.cloud_service_type_resource})

    def collect_resources(self, params: Dict) -> Union[Iterator[CloudServiceResponse],
                                                       Iterator[CloudServiceTypeResourceResponse]]:

        if 'secret_data' not in params:
            raise CollectorError(message='secret_data key must exist in params')

        self._set_connection(params.get('secret_data'))

        options = params.get('options')

        self._create_resource_objs(options)

        for resource_obj in self._resource_obj_list:
            yield self._create_cloud_sevice_type_response(resource_obj)

        for collected_obj_resources in self._collect_objs_resources():
            yield from self._create_cloud_sevice_responses(collected_obj_resources)

