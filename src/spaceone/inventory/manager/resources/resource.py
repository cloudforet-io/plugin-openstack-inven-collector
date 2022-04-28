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
    _project_resource: str = ""
    _dashboard_url: Optional[str] = None
    _collaboration_resources: List['BaseResource'] = []

    def __init__(self, conn: Connection, **kwargs):
        self._conn = conn
        self._dashboard_url = None
        self._external_link = ""

        if kwargs.get('secret_data'):
            if 'dashboard_url' in kwargs.get('secret_data'):
                self._dashboard_url = kwargs.get('secret_data').get('dashboard_url')

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
    def external_link(self) -> str:

        if self._dashboard_url is None:
            return None

        return urljoin(self._dashboard_url, self._project_resource)

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

    def _set_default_model_obj_values(self, model_obj: Any, resource: Any):
        pass

    def _set_default_model_obj_reference(self, model_obj: Any, resource: Any):

        if hasattr(resource, 'links'):

            dic = {}

            for link in resource.links:
                if link['rel'] == 'self':
                    dic['self_link'] = link['href']

                if link['rel'] == 'bookmark':
                    dic['bookmark_link'] = link['href']

                if self.external_link is not None:
                    dic['external_link'] = urljoin(self.external_link, resource.id)

            self._set_obj_key_value(model_obj, 'reference', ReferenceModel(dic))

    def _create_obj(self, model_cls: ResourceModel, resource: Resource) -> (ResourceModel, Resource):

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
        self._set_default_model_obj_reference(model_obj, resource)

        return model_obj

    def collect(self, **kwargs) -> Iterator[Tuple[ResourceModel, 'BaseResource']]:

        for resource in self.resources:
            _LOGGER.debug(resource.to_dict())
            yield self._create_obj(self._model_cls, resource), self
