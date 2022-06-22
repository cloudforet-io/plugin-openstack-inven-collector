import copy
from typing import (
    List,
    Optional,
    Type
)

from spaceone.inventory.model.view.dynamic_field import *

# all openstack resources
OS_RESOURCE_MAP = {
    "InstanceResource": "spaceone.inventory.manager.resources.compute",
    "HypervisorResource": "spaceone.inventory.manager.resources.hypervisor",
    "VolumeResource": "spaceone.inventory.manager.resources.block_storage",
    "NetworkResource": "spaceone.inventory.manager.resources.network",
    "SubnetResource": "spaceone.inventory.manager.resources.network",
    "SecurityGroupResource": "spaceone.inventory.manager.resources.security_group",
    "ShareResource": "spaceone.inventory.manager.resources.share",
    "ShareNetworkResource": "spaceone.inventory.manager.resources.share",
    "ProjectResource": "spaceone.inventory.manager.resources.project",
    "UserResource": "spaceone.inventory.manager.resources.user",
    "RoleResource": "spaceone.inventory.manager.resources.user",
    "RoleAssignmentResource": "spaceone.inventory.manager.resources.user",
    "ComputeQuotaResource": "spaceone.inventory.manager.resources.compute",
    "VolumeQuotaResource": "spaceone.inventory.manager.resources.block_storage",
    "ComputeAZResource": "spaceone.inventory.manager.resources.compute",
    "StorageResource": "spaceone.inventory.manager.resources.storage",
    "FloatingIPResource": "spaceone.inventory.manager.resources.network",
    "RouterResource": "spaceone.inventory.manager.resources.network",
    "ImageResource": "spaceone.inventory.manager.resources.image",
    "SnapshotResource": "spaceone.inventory.manager.resources.block_storage",
    "ServerGroupResource": "spaceone.inventory.manager.resources.compute",

}


class CSTMeta:

    def __init__(self, field_cls_name: str, name: str, key: str, **kwargs):

        self.field_cls: Type[BaseDynamicField] = self.get_resource_class(field_cls_name)
        self.name: str = name
        self.key: str = key
        self.data_type = None
        self.kwargs = kwargs
        self.field: BaseDynamicField = self.field_cls.data_source(name, key, **kwargs)
        self.search: Optional[SearchField] = None

        if 'data_type' in kwargs:

            if kwargs.get('data_type') == int:
                self.data_type = 'integer'

            if kwargs.get('data_type') == float:
                self.data_type = 'float'

        if 'auto_search' in kwargs and kwargs.get('auto_search'):

            search_key = key

            if kwargs.get('options'):
                options = kwargs.get('options')

                if options.get('sub_key'):
                    search_key = f"{search_key}.{options.get('sub_key')}"

            if self.data_type:
                self.search = SearchField.set(name=name, key=search_key, data_type=self.data_type)
            else:
                self.search = SearchField.set(name=name, key=search_key)

    @staticmethod
    def get_resource_class(class_name: str) -> Type[BaseDynamicField]:
        module_name = "spaceone.inventory.model.view.dynamic_field"
        mod = __import__(module_name, fromlist=[module_name])
        cls = getattr(mod, class_name)
        return cls

    def __eq__(self, name: object):
        if not isinstance(name, str):
            raise NotImplementedError

        if name == self.name:
            return True

        return False


class CSTMetaGenerator:
    cst_meta_list: List[CSTMeta] = []

    def __init__(self, cst_meta_generator: Optional['CSTMetaGenerator'] = None, **kwargs):
        self.cst_meta_list = []

        if cst_meta_generator:
            self.cst_meta_list = copy.copy(cst_meta_generator.cst_metas)

    @staticmethod
    def _create_cst_meta(field_cls_name: str, name: str, key: str, **kwargs) -> CSTMeta:
        return CSTMeta(field_cls_name, name, key, **kwargs)

    def _get_cst_field_index(self, name: str) -> int:
        return self.cst_meta_list.index(name)

    def insert_cst_meta_field(self, previous_field_name: str, field_cls_name: str, name: str, key: str,
                              **kwargs) -> None:

        cst_meta = self._create_cst_meta(field_cls_name, name, key, **kwargs)
        previous_field_index = self._get_cst_field_index(previous_field_name)
        self.cst_meta_list.insert(previous_field_index + 1, cst_meta)

    def append_cst_meta_field(self, field_cls_name: str, name: str, key: str, **kwargs) -> None:

        cst_meta = self._create_cst_meta(field_cls_name, name, key, **kwargs)

        if kwargs.get('index'):
            self.cst_meta_list.insert(kwargs.get('index'), cst_meta)
        else:
            self.cst_meta_list.append(cst_meta)

    def delete_cst_meta_field(self, name: str) -> None:
        self.cst_meta_list.remove(name)

    @property
    def cst_metas(self) -> List[CSTMeta]:
        return self.cst_meta_list

    @property
    def fields(self) -> List[BaseDynamicField]:

        field_list = []

        for cst_meta in self.cst_meta_list:
            field_list.append(cst_meta.field)

        return field_list

    def get_table_fields(self, **kwargs) -> List[BaseDynamicField]:

        field_list = []

        for cst_meta in self.cst_meta_list:
            options = cst_meta.kwargs.get('options')

            if kwargs.get("ignore_optional"):
                if options and options.get('is_optional'):
                    continue

            key = cst_meta.key
            field_cls = cst_meta.field_cls

            if kwargs.get("ignore_data_path"):
                splitted_keys = key.split(".")

                if splitted_keys and splitted_keys[0] == 'data':
                    splitted_keys.remove('data')
                    key = ".".join(splitted_keys)

            if kwargs.get("add_root_path"):
                add_key_path = kwargs.get("add_root_path")
                key = f"{add_key_path}.{key}"

            field = field_cls.data_source(cst_meta.name, key, **cst_meta.kwargs)
            field_list.append(field)

        return field_list

    @property
    def search(self) -> List[SearchField]:

        search_list = []

        for cst_meta in self.cst_meta_list:
            if cst_meta.search:
                search_list.append(cst_meta.search)

        return search_list
