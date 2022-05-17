import logging
from typing import (
    List,
    Dict,
    Optional,
    Union,
    Tuple,
    Callable,
    Iterator
)

import openstack
import json
from openstack.connection import Connection
from spaceone.core.manager import BaseManager
from spaceone.inventory.manager import resources
from spaceone.inventory.model.common.base import CloudServiceReferenceModel
from spaceone.inventory.model.common.base import CloudServiceResource
from spaceone.inventory.model.common.response import CloudServiceResponse
from spaceone.inventory.model.common.response import CloudServiceTypeResourceResponse
from spaceone.inventory.model.resources.base import ResourceModel
from spaceone.inventory.model.resources.base import Secret
from spaceone.inventory.error.base import CollectorError

_LOGGER = logging.getLogger(__name__)

__all__ = ['OpenstackManager']


class OpenstackManager(BaseManager):

    _resource_cls_list: List[Callable[[Optional[Connection]], 'BaseResource']] = []
    _resource_obj_list: List['BaseResource'] = []
    _secret_data: Dict = {}
    _options: Dict = {}
    __conn: Optional[Connection] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._resource_obj_list = []
        self._resource_cls_list = []
        self._secret_data = {}
        self._options = {}
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

    def _set_resource_cls(self) -> None:

        for class_name, module_name in resources.OS_RESOURCE_MAP.items():
            mod = __import__(module_name, fromlist=[module_name])
            cls = getattr(mod, class_name)
            self._resource_cls_list.append(cls)

    def _set_connection(self, secret_data: Optional[Dict] = {}) -> None:

        # Initialize and turn on debug logging

        openstack.enable_logging(debug=False)

        if secret_data is None:
            raise CollectorError(message='The secret data must exist for connection.')

        try:

            self._secret_data = Secret(secret_data)
            self._secret_data.validate()

            self.conn = openstack.connection.Connection(
                region_name=self._secret_data.region_name,
                auth=dict(
                    auth_url=self._secret_data.auth_url,
                    username=self._secret_data.username,
                    password=self._secret_data.password,
                    project_id=self._secret_data.project_id,
                    user_domain_name=self._secret_data.user_domain_name),
                identity_api_version=self._secret_data.identity_api_version,
                interface=self._secret_data.interface)

        except Exception as e:
            raise CollectorError(message='Creating openstack connection failed', cause=e)

    def _create_resource_objs(self, **kwargs) -> None:

        cloud_service_types = []

        options = kwargs.get('options')

        if options and options.get('cloud_service_types'):
            if isinstance(options.get('cloud_service_types'), list):
                cloud_service_types = options.get('cloud_service_types')

        _LOGGER.info(f"Collect target cloud service types : {cloud_service_types}")

        # Add resources object type for collecting
        self._set_resource_cls()

        _LOGGER.info(f"Total resource class list : {self._resource_cls_list}")

        dic = {}

        if kwargs.get('secret_data'):
            if 'all_projects' in kwargs.get('secret_data'):
                dic['all_projects'] = json.loads(kwargs.get('secret_data').get('all_projects').lower())

            # for dev test
            #dic['all_projects'] = True

            if 'dashboard_url' in kwargs.get('secret_data'):
                dic['dashboard_url'] = kwargs.get('secret_data').get('dashboard_url')

        for resource_cls in self._resource_cls_list:
            resource_obj = resource_cls(self.conn, **dic)

            if len(cloud_service_types) == 1 and cloud_service_types[0] == '*':
                self._resource_obj_list.append(resource_obj)
            elif len(cloud_service_types) == 0 or resource_obj.cloud_service_type_name in cloud_service_types:
                self._resource_obj_list.append(resource_obj)

            if resource_obj:
                _LOGGER.info(f"Resource Added : {resource_obj.cloud_service_type_name}")

    def _collect_objs_resources(self) -> Iterator[List[ResourceModel]]:

        for resource_obj in self._resource_obj_list:
            yield resource_obj.collect(collect_associated_resource=True)

    def _create_cloud_service_responses(self, collected_resources: List[Tuple[ResourceModel, 'BaseResource']]) \
            -> Iterator[CloudServiceResponse]:

        for collected_resource_model, resource_obj in collected_resources:

            # resource_id must exist in reference
            instance_size: str = None
            name: str = None
            project_id: str = None
            reference = CloudServiceReferenceModel({"resource_id": collected_resource_model.id})

            if hasattr(collected_resource_model, 'external_link') and \
                    getattr(collected_resource_model, 'external_link'):
                reference.external_link = collected_resource_model.external_link

            if hasattr(collected_resource_model, 'size') and \
                    getattr(collected_resource_model, 'size'):
                instance_size = collected_resource_model.size

            if hasattr(collected_resource_model, 'name') and \
                    getattr(collected_resource_model, 'name'):
                name = collected_resource_model.name

            if hasattr(collected_resource_model, 'project_id') and \
                    getattr(collected_resource_model, 'project_id'):
                project_id = collected_resource_model.project_id

            resource = CloudServiceResource({'data': collected_resource_model,
                                             'name': name,
                                             'account': project_id,
                                             'reference': reference,
                                             'region_code': self.region_code,
                                             '_metadata': resource_obj.cloud_service_meta,
                                             'cloud_service_group': resource_obj.cloud_service_group_name,
                                             'cloud_service_type': resource_obj.cloud_service_type_name,
                                             'instance_size': instance_size})

            _LOGGER.debug(resource.to_primitive())
            yield CloudServiceResponse({'resource': resource})

    def collect_resources(self, params: Dict) -> Union[Iterator[CloudServiceResponse],
                                                       Iterator[CloudServiceTypeResourceResponse]]:

        if 'secret_data' not in params:
            raise CollectorError(message='secret_data key must exist in params')

        self._set_connection(params.get('secret_data'))

        self._create_resource_objs(secret_data=params.get('secret_data'), options=params.get('options'))

        for resource_obj in self._resource_obj_list:
            cloud_svc_type_response =\
                CloudServiceTypeResourceResponse({"resource": resource_obj.cloud_service_type_resource})
            _LOGGER.debug(cloud_svc_type_response.to_primitive())
            yield cloud_svc_type_response

        for collected_obj_resources in self._collect_objs_resources():
            yield from self._create_cloud_service_responses(collected_obj_resources)
