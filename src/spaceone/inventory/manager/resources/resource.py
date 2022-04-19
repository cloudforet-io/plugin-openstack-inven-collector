import logging
from schematics import Model
from schematics.types import DateTimeType
from spaceone.inventory.model import ResourceModel
from openstack.resource import Resource
from openstack.connection import Connection
from openstack.proxy import Proxy

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
    Iterator
)

_LOGGER = logging.getLogger(__name__)


class BaseResource(object):
    _conn: Optional[Connection] = None
    _model_cls: Any = ResourceModel
    _proxy: str = ""
    _resource: str = ""
    _datetime_keys: List[str] = ['attached_at', 'created_at', 'updated_at', 'launched_at']

    def __init__(self, conn: Connection):
        self._conn = conn

    @property
    def resources(self) -> List[Any]:

        if self._conn is None:
            raise

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

    def _create_obj(self, model_cls: ResourceModel, resource: Resource) -> ResourceModel:

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

        return model_obj

    def collect(self, **kwargs) -> List[ResourceModel]:

        resources = []

        for resource in self.resources:
            _LOGGER.debug(resource.to_dict())
            resources.append(self._create_obj(self._model_cls, resource))

        return resources
