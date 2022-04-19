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
from spaceone.inventory.model import ResourceModel
from openstack.connection import Connection
from spaceone.inventory.error.base import CollectorError

from typing import (
    Any,
    Iterable,
    List,
    Dict,
    Optional,
    Type,
    Union,
    Tuple,
    Callable,
    Generator,
    Iterator
)

_LOGGER = logging.getLogger(__name__)

__all__ = ['OpenstackManager']


class OpenstackManager(BaseManager):
    _resource_obj_list: List[BaseResource] = []
    _resource_cls_list: List[Any] = [InstanceResource, VolumeResource, NetworkResource, FlavorResource]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__conn = None

    @property
    def conn(self):
        return self.__conn

    @conn.setter
    def conn(self, conn: Connection = None):
        self.__conn = conn

    def _set_connection(self, secret_data: Optional[Dict] = {}):

        # Initialize and turn on debug logging

        openstack.enable_logging(debug=False)

        if secret_data is None:
            raise CollectorError(message='secret_data must exist')

        try:
            username = secret_data.get('username')
            password = secret_data.get('password')
            user_domain_name = secret_data.get('user_domain_name')
            auth_url = secret_data.get('auth_url')
            project_id = secret_data.get('project_id')
            identity_api_version = secret_data.get('identity_api_version')
            interface = secret_data.get('interface')
            region_name = secret_data.get('region_name')

            # Initialize connection
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

    def _create_resource_obj(self, openstack_resource_class: Callable[[Optional[Connection]], 'BaseResource']):

        resource_obj = openstack_resource_class(self.conn)
        self._resource_obj_list.append(resource_obj)

    def _create_resource_objs(self):

        # Add resource type for collecting
        for resource_cls in self._resource_cls_list:
            self._create_resource_obj(resource_cls)

    def _collect_objs_resources(self) -> Iterator[List[ResourceModel]]:

        for resource_obj in self._resource_obj_list:
            yield resource_obj.collect()

    def _create_cloud_svc_responses(self, collected_resources: List[ResourceModel]) -> Iterator[CloudServiceResponse]:

        for collected_resource in collected_resources:
            yield CloudServiceResponse({'resource': collected_resource})

    def collect_resources(self, params: Dict = {}) -> Iterator[CloudServiceResponse]:

        if 'secret_data' not in params:
            raise CollectorError(message='secret_data key must exist in params')

        self._set_connection(params.get('secret_data'))
        self._create_resource_objs()

        for collected_obj_resources in self._collect_objs_resources():
            yield from self._create_cloud_svc_responses(collected_obj_resources)
