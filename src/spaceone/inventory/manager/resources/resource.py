from typing import (
    Any,
    List,
    Optional,
    Tuple,
    Iterator,
    Final,
    Generator,
    Type,
)
from urllib.parse import urljoin
from urllib.parse import urlparse

from openstack.connection import Connection
from openstack.resource import Resource
from schematics.types import DateTimeType

from spaceone.inventory.conf.settings import get_logger
from spaceone.inventory.error.base import CollectorError
from spaceone.inventory.manager import resources
from spaceone.inventory.model.common.response import CloudServiceTypeResource
from spaceone.inventory.model.resources.base import ReferenceModel
from spaceone.inventory.model.resources.base import ResourceModel
from spaceone.inventory.model.view.cloud_service import CloudServiceMeta

_LOGGER = get_logger(__name__)

DATETIME_KEYS: Final[List[str]] = ['attached_at', 'created_at', 'updated_at', 'launched_at', 'password_expires_at']


class BaseResource(object):
    _model_cls: Type[ResourceModel] = ResourceModel
    _proxy: str = ""
    _resource: str = ""
    _cloud_service_type_resource: Optional[CloudServiceTypeResource] = None
    _cloud_service_meta: Optional[CloudServiceMeta] = None
    _is_admin_dashboard: bool = True
    _resource_path: str = ""
    _associated_resource_cls_list: List[str] = []
    _native_all_projects_query_support: bool = False
    _native_project_id_query_support: bool = False
    _project_key: str = 'project_id'

    def __init__(self, conn: Connection, *args, **kwargs):
        self._conn: Connection = conn
        self._dashboard_url: Optional[str] = None
        self._all_projects: bool = False
        self._associated_resource_list: List[Tuple[ResourceModel, 'BaseResource']] = []
        self._projects: dict = {}
        self._default_args: tuple = args
        self._default_kwargs: dict = kwargs
        self._admin_project_id: Optional[str] = None
        self._is_associated_resource: bool = False

        if kwargs.get('all_projects'):
            self._all_projects = bool(kwargs.get('all_projects'))

        try:
            # for getting project name
            for project in self._conn.identity.projects():
                self._projects[project.id] = {"name": project.name}

                if project.name == 'admin':
                    self._admin_project_id = project.id

        except Exception as e:
            _LOGGER.info(e)

    def get_location_project_id(self, resource: Resource) -> Optional[str]:

        location = resource.get("location")

        if location and location.get("project"):
            project = location.get("project")
            if project and project.get('id'):
                return location.get("project").get("id")

        return None

    @staticmethod
    def get_resource_class(class_name: str) -> Type['BaseResource']:
        module_name = resources.OS_RESOURCE_MAP[class_name]
        mod = __import__(module_name, fromlist=[module_name])
        cls = getattr(mod, class_name)
        return cls

    @property
    def admin_project_id(self) -> Optional[str]:
        return self._admin_project_id

    @property
    def is_associated_resource(self) -> bool:
        return self._is_associated_resource

    @is_associated_resource.setter
    def is_associated_resource(self, value: bool) -> None:
        self._is_associated_resource = value


    @property
    def args(self) -> tuple:
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
        return self.__class__.__name__

    @property
    def cloud_service_meta(self) -> Optional[CloudServiceMeta]:
        return self._cloud_service_meta

    @property
    def cloud_service_type_resource(self) -> Optional[CloudServiceTypeResource]:
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
    def dashboard_url(self) -> Optional[str]:
        return self._dashboard_url

    @dashboard_url.setter
    def dashboard_url(self, value: str) -> None:
        self._dashboard_url = value

    @property
    def resource_path(self) -> str:
        return self._resource_path

    @property
    def resources(self) -> List[Resource]:

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

                    resources_list: List[Resource] = []

                    for project_id in self._projects.keys():
                        kwargs[self._project_key] = project_id
                        rtn = resource_method(*args, **kwargs)

                        if isinstance(rtn, list) or isinstance(rtn, Generator):
                            resources_list += rtn
                        else:
                            resources_list.append(rtn)

                    return resources_list

                return resource_method(*args, **kwargs)

        return []

    @staticmethod
    def _set_obj_key_value(obj: Any, key: str, value: Any) -> None:
        setattr(obj, key, value)

    # for sub class custom values
    def _set_custom_model_obj_values(self, model_obj: ResourceModel, resource: Resource) -> None:
        pass

    def __set_default_model_obj_project(self, model_obj: ResourceModel, resource: Resource) -> None:

        if self._projects.get(resource.get('project_id'), None):
            project_id = resource.get('project_id')
            project_name = self._projects[project_id].get("name")
            self._set_obj_key_value(model_obj, 'project_name', project_name)

    def __set_default_model_obj_location(self, model_obj: ResourceModel, resource: Resource) -> None:

        location = resource.get('location')

        if location and location.get('region_name'):
            self._set_obj_key_value(model_obj, 'region_name', location.get('region_name'))

    def __set_default_model_obj_links(self, model_obj: ResourceModel, resource: Resource) -> None:

        if resource.get('links'):

            dic = {}

            if isinstance(resource.get('links'), list):
                for link in resource.links:
                    if link['rel'] == 'self':
                        dic['self_link'] = link['href']

                    if link['rel'] == 'bookmark':
                        dic['bookmark_link'] = link['href']

            elif isinstance(resource.get('links'), dict):
                if resource.links.get('self'):
                    dic['self_link'] = resource.links.get('self')

                if resource.links.get('bookmark'):
                    dic['bookmark_link'] = resource.links.get('bookmark')

            self._set_obj_key_value(model_obj, 'reference', ReferenceModel(dic))

        if self.dashboard_url and self.resource_path:

            kwargs = model_obj.to_primitive()

            dashboard_url = urlparse(self.dashboard_url)
            dashboard_url_path = dashboard_url.path

            external_base = f"{dashboard_url.scheme}://{dashboard_url.netloc}"

            if self._is_admin_dashboard:
                kwargs['project_id'] = self.admin_project_id

            external_url = ''

            if 'project_id' in kwargs:
                external_url = "/".join(
                    (dashboard_url_path.strip('/'), 'auth/switch/{project_id}/?next='.format(**kwargs)))

            resource_url = BaseResource.urljoin(dashboard_url_path, self.resource_path.format(**kwargs))
            external_url = BaseResource.urljoin(external_url, resource_url)

            self._set_obj_key_value(model_obj, 'external_link', urljoin(base=external_base, url=external_url))

    @staticmethod
    def urljoin(*args) -> str:
        return "/".join(map(lambda x: str(x).lstrip('/'), args))

    def get_resource_model_from_associated_resource(self, resource_cls_name: str, **kwargs) \
            -> Optional[ResourceModel]:

        for resource_model, resource in self._associated_resource_list:
            if resource.__class__.__name__ == resource_cls_name:
                matched = True

                for key, value in kwargs.items():
                    if hasattr(resource_model, key) and getattr(resource_model, key) != value:
                        matched = False
                        continue

                if matched:
                    return resource_model

        return None

    def get_resource_model_from_associated_resources(self, resource_cls_name: str, **kwargs) \
            -> List[ResourceModel]:

        rtn_list = []

        for resource_model, resource in self._associated_resource_list:
            if resource.__class__.__name__ == resource_cls_name:
                # Default is True if search key not exists.
                matched = True
                for key, value in kwargs.items():

                    if (hasattr(resource_model, key) and getattr(resource_model, key) != value) or \
                            not hasattr(resource_model, key):
                        matched = False
                        continue

                    if hasattr(resource_model, key) and getattr(resource_model, key) == value:
                        matched = True

                if matched:
                    rtn_list.append(resource_model)

        return rtn_list

    def _collect_associated_resource(self, *args, **kwargs) -> None:

        for class_name in self._associated_resource_cls_list:
            associated_resource = self.get_resource_class(class_name)(self._conn, *args, **kwargs)
            associated_resource.is_associated_resource = True

            if associated_resource:
                _LOGGER.info(f"Collecting related resources : {associated_resource.resource_name}")

            if self.all_projects:
                associated_resource.all_projects = True

            try:
                for resource in associated_resource.collect():
                    self._associated_resource_list.append(resource)
            except Exception as e:
                _LOGGER.error(e)
                raise

    def _create_obj(self, model_cls: Type[ResourceModel], resource: Resource, **kwargs) -> ResourceModel:

        model_obj = model_cls()

        if isinstance(resource, dict):
            resource_dic = resource
        else:
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
        self.__set_default_model_obj_location(model_obj, resource)

        return model_obj

    def collect(self, **kwargs) -> Iterator[Tuple[ResourceModel, 'BaseResource']]:

        collect_associated_resource = kwargs.get('collect_associated_resource')

        # for openstack manager collection request only
        if collect_associated_resource:
            _LOGGER.info(f"Start collecting resources : {self.resource_name}")
            self._collect_associated_resource()

        try:
            _LOGGER.info(f"Customizing collected resource : {self.resource_name}")

            for resource in self.resources:
                yield self._create_obj(self._model_cls, resource), self

        except Exception as e:
            if e.__class__.__name__ == "EndpointNotFound":
                _LOGGER.info(f"{self.resource_name} : {e}")
            else:
                _LOGGER.error(f"{self.resource_name} : {e}")
                raise
        finally:
            if collect_associated_resource:
                _LOGGER.info(f"Collecting resources is done. : {self.resource_name} ")
