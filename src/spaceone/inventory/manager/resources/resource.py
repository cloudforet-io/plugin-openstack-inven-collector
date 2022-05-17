import logging
import json
from typing import (
    Any,
    List,
    Dict,
    Optional,
    Tuple,
    Iterator,
    Final
)
from urllib.parse import urljoin

from openstack.connection import Connection
from openstack.resource import Resource
from schematics.types import DateTimeType

from spaceone.inventory.manager import resources
from spaceone.inventory.error.base import CollectorError
from spaceone.inventory.model.common.response import CloudServiceTypeResource
from spaceone.inventory.model.resources.base import ReferenceModel

from spaceone.inventory.model.resources.base import ResourceModel
from spaceone.inventory.model.view.cloud_service import CloudServiceMeta

_LOGGER = logging.getLogger(__name__)

DATETIME_KEYS: Final[List[str]] = ['attached_at', 'created_at', 'updated_at', 'launched_at']


class BaseResource(object):
    _model_cls: Any = ResourceModel
    _proxy: str = ""
    _resource: str = ""
    _cloud_service_type_resource: Optional[CloudServiceTypeResource] = None
    _cloud_service_meta: Optional[CloudServiceMeta] = None
    _resource_path: Final[str] = ""
    _native_all_projects_query_support: Final[bool] = False
    _native_project_id_query_support: Final[bool] = False

    def __init__(self, conn: Connection, **kwargs):
        self._conn: Connection = conn
        self._dashboard_url: Optional[str] = None
        self._all_projects: bool = False
        self._associated_resource_cls_list: List['BaseResource'] = []
        self._associated_resource_list: List[Tuple[ResourceModel, 'BaseResource']] = []
        self._projects: Dict[str] = {}
        self._default_args: Tuple = ()
        self._default_kwargs: Dict = {}

        if 'default_args' in kwargs:
            self._default_args = kwargs.get('default_args')

        if 'default_kwargs' in kwargs:
            self.default_kwargs = kwargs.get('default_kwargs')

        if 'all_projects' in kwargs:
            self._all_projects = kwargs.get('all_projects')

        if 'dashboard_url' in kwargs:
            self._dashboard_url = kwargs.get('dashboard_url')

        try:
            # for getting project name
            for project in self._conn.identity.projects():
                self._projects[project.id] = {"name": project.name}

        except Exception as e:
            _LOGGER.info(e)

    @staticmethod
    def get_resource_class(class_name):
        module_name = resources.OS_RESOURCE_MAP[class_name]
        mod = __import__(module_name, fromlist=[module_name])
        cls = getattr(mod, class_name)
        return cls

    @property
    def args(self):
        return self._default_args

    @args.setter
    def args(self, value: tuple) -> None:
        self._default_args = value

    @property
    def all_projects(self) -> bool:
        return self._all_projects

    @all_projects.setter
    def all_projects(self, value: bool) -> None:
        self._all_projects = value

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
        if self._cloud_service_type_resource:
            return self._cloud_service_type_resource.name
        return ""

    @property
    def cloud_service_group_name(self) -> str:
        if self._cloud_service_type_resource:
            return self._cloud_service_type_resource.group
        return ""

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

                kwargs = self._default_kwargs.copy()
                args = list(self._default_args).copy()

                if self._all_projects and self._native_all_projects_query_support:
                    kwargs['all_projects'] = self._all_projects

                if self._all_projects and not self._native_all_projects_query_support \
                        and self._native_project_id_query_support:

                    resources_list = []
                    for project_id in self._projects.keys():
                        kwargs['project_id'] = project_id
                        resources_list += resource_method(*args, **kwargs)
                    return resources_list

                return resource_method(*args, **kwargs)

        return []

    @staticmethod
    def _set_obj_key_value(obj: Any, key: str, value: Any) -> None:
        setattr(obj, key, value)

    # for sub class custom values
    def _set_custom_model_obj_values(self, model_obj: Any, resource: Any):
        pass

    def __set_default_model_obj_project(self, model_obj: Any, resource: Any):

        if self._projects.get(resource.get('project_id'), None):
            project_id = resource.get('project_id')
            project_name = self._projects[project_id].get("name")
            self._set_obj_key_value(model_obj, 'project_name', project_name)

    def __set_default_model_obj_region(self, model_obj: Any, resource: Any):

        if resource.get('location') and resource.location.get('region_name'):
            self._set_obj_key_value(model_obj, 'region_name', resource.location.region_name)

    def __set_default_model_obj_links(self, model_obj: Any, resource: Any):

        if resource.get('links'):

            dic = {}

            for link in resource.links:
                if link['rel'] == 'self':
                    dic['self_link'] = link['href']

                if link['rel'] == 'bookmark':
                    dic['bookmark_link'] = link['href']

            self._set_obj_key_value(model_obj, 'reference', ReferenceModel(dic))

        if self.external_url and self._resource_path:

            kwargs = {}

            if resource.get('id'):
                kwargs['id'] = resource.get('id')

            if resource.get('name'):
                kwargs['name'] = resource.get('name')

            if resource.get('project_id'):
                kwargs['project_id'] = resource.get('project_id')

            self._set_obj_key_value(model_obj, 'external_link', urljoin(base=self.external_url,
                                                                        url=self._resource_path.format(**kwargs)))

    def get_resource_model_from_associated_resource(self, resource_type: str, **kwargs) \
            -> Optional[ResourceModel]:

        for resource_model, resource in self._associated_resource_list:
            if resource.resource_name == resource_type:
                matched = True

                for key, value in kwargs.items():
                    if hasattr(resource_model, key) and getattr(resource_model, key) != value:
                        matched = False
                        continue

                if matched:
                    return resource_model

        return None

    def get_resource_model_from_associated_resources(self, resource_type: str, **kwargs) \
            -> Optional[ResourceModel]:

        rtn_list = []

        for resource_model, resource in self._associated_resource_list:
            if resource.resource_name == resource_type:
                matched = True
                for key, value in kwargs.items():
                    if hasattr(resource_model, key) and getattr(resource_model, key) != value:
                        matched = False
                        continue

                if matched:
                    rtn_list.append(resource_model)

        return rtn_list

    def _collect_associated_resource(self, **kwargs):

        for class_name in self._associated_resource_cls_list:
            associated_resource = self.get_resource_class(class_name)(self._conn, **kwargs)

            if self.all_projects:
                associated_resource.all_projects = True
            try:
                for resource in associated_resource.collect():
                    self._associated_resource_list.append(resource)
            except Exception as e:
                _LOGGER.error(e)

    def _create_obj(self, model_cls: ResourceModel, resource: Resource, **kwargs) -> (ResourceModel, Resource):

        model_obj = model_cls()

        resource_dic = resource.to_dict()

        for key, value in resource_dic.items():
            if hasattr(model_obj, key):
                if key in DATETIME_KEYS and value:
                    dt_value = DateTimeType().to_native(value)
                    setattr(model_obj, key, dt_value)
                else:
                    setattr(model_obj, key, value)

        self._set_custom_model_obj_values(model_obj, resource)
        self.__set_default_model_obj_links(model_obj, resource)
        self.__set_default_model_obj_project(model_obj, resource)
        self.__set_default_model_obj_region(model_obj, resource)

        return model_obj

    def collect(self, **kwargs) -> Iterator[Tuple[ResourceModel, 'BaseResource']]:

        # for openstack manager collection request only
        if kwargs.get('collect_associated_resource'):
            self._collect_associated_resource()

        try:
            for resource in self.resources:
                yield self._create_obj(self._model_cls, resource), self
        except Exception as e:
            _LOGGER.error(e)
