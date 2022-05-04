import logging
from schematics import Model
from schematics.types import DateTimeType
from spaceone.inventory.model.resources.base import ResourceModel
from openstack.resource import Resource
from openstack.connection import Connection
from openstack.proxy import Proxy
from spaceone.inventory.error.base import CollectorError
from spaceone.inventory.model.common.response import CloudServiceTypeResource
from spaceone.inventory.model.view.cloud_service import CloudServiceMeta
from spaceone.inventory.model.resources.base import ReferenceModel
from urllib.parse import urljoin

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
    TypeVar,
    Iterator,
    Final
)

_LOGGER = logging.getLogger(__name__)


class BaseResource(object):
    _datetime_keys: Final[List[str]] = ['attached_at', 'created_at', 'updated_at', 'launched_at']
    _model_cls: Any = ResourceModel
    _conn: Optional[Connection] = None
    _proxy: str = ""
    _resource: str = ""
    _cloud_service_type_resource: Optional[CloudServiceTypeResource] = None
    _cloud_service_meta: Optional[CloudServiceMeta] = None
    _resource_path: Optional[str] = None
    _dashboard_url: Optional[str] = None
    _associated_resource_cls_list: List['BaseResource'] = []
    _associated_resource_list: List[Tuple[ResourceModel, 'BaseResource']] = []

    def __init__(self, conn: Connection, **kwargs):
        self._conn = conn
        self._dashboard_url = None

        if kwargs.get('secret_data'):
            if 'dashboard_url' in kwargs.get('secret_data'):
                self._dashboard_url = kwargs.get('secret_data').get('dashboard_url')

    @property
    def resource_name(self) -> str:
        return self._resource

    @property
    def cloud_service_meta(self) -> CloudServiceMeta:
        return self._cloud_service_meta

    @property
    def cloud_service_type_resource(self) -> CloudServiceTypeResource:
        return self._cloud_service_type_resource

    @property
    def cloud_service_type_name(self) -> str:
        return self._cloud_service_type_resource.name

    @property
    def cloud_service_group_name(self) -> str:
        return self._cloud_service_type_resource.group

    @property
    def external_url(self) -> str:

        if self._dashboard_url is None:
            return None

        return urljoin(base=self._dashboard_url, url=self._resource_path)

    @property
    def resources(self) -> List[Any]:

        if self._conn is None:
            raise CollectorError(message='secret_data must exist')

        if hasattr(self._conn, self._proxy):
            proxy_obj = getattr(self._conn, self._proxy)
            if hasattr(proxy_obj, self._resource):
                resource_method = getattr(proxy_obj, self._resource)
                return resource_method()

        return []

    @staticmethod
    def _set_obj_key_value(obj: Any, key: str, value: Any) -> None:
        setattr(obj, key, value)

    # for sub class custom values
    def _set_default_model_obj_values(self, model_obj: Any, resource: Any):
        pass

    def __set_default_model_obj_region(self, model_obj: Any, resource: Any):

        if hasattr(resource, 'location') and hasattr(resource.location, 'region_name'):
            self._set_obj_key_value(model_obj, 'region_name', resource.location.region_name)

    def __set_default_model_obj_links(self, model_obj: Any, resource: Any):

        if hasattr(resource, 'links'):

            dic = {}

            for link in resource.links:
                if link['rel'] == 'self':
                    dic['self_link'] = link['href']

                if link['rel'] == 'bookmark':
                    dic['bookmark_link'] = link['href']

            self._set_obj_key_value(model_obj, 'reference', ReferenceModel(dic))

        if self.external_url and self._resource_path:
            self._set_obj_key_value(model_obj, 'external_link', urljoin(base=self.external_url,
                                                                        url=self._resource_path.format(id=resource.id)))

    def get_resource_model_from_associated_resources(self, resource_name: str, resource_id: str) \
            -> Optional[ResourceModel]:

        for resource_model, resource in self._associated_resource_list:
            if resource.resource_name == resource_name and resource_model.id == resource_id:
                return resource_model

        return None

    def _collect_associated_resource(self):

        for associated_resource_cls in self._associated_resource_cls_list:
            for resource in associated_resource_cls(self._conn).collect():
                self._associated_resource_list.append(resource)

    def _create_obj(self, model_cls: ResourceModel, resource: Resource, **kwargs) -> (ResourceModel, Resource):

        model_obj = model_cls()

        resource_dic = resource.to_dict()

        for key, value in resource_dic.items():
            if hasattr(model_obj, key):
                if key in self._datetime_keys:
                    dt_value = DateTimeType().to_native(value)
                    setattr(model_obj, key, dt_value)
                else:
                    setattr(model_obj, key, value)

        self._set_default_model_obj_values(model_obj, resource)
        self.__set_default_model_obj_links(model_obj, resource)
        self.__set_default_model_obj_region(model_obj, resource)

        return model_obj

    def collect(self, **kwargs) -> Iterator[Tuple[ResourceModel, 'BaseResource']]:

        if kwargs.get('collect_associated_resource'):
            self._collect_associated_resource()

        for resource in self.resources:
            yield self._create_obj(self._model_cls, resource), self
