import copy
from typing import (
    List,
    Optional,
)

from spaceone.inventory.model.view.dynamic_field import BaseDynamicField
from spaceone.inventory.model.view.dynamic_field import SearchField


class CSTMeta:

    def __init__(self, field_cls: BaseDynamicField, name: str, key: str, **kwargs):
        self.field_cls = field_cls
        self.name: str = name
        self.key: str = key
        self.data_type = None
        self.kwargs = kwargs
        self.field: BaseDynamicField = field_cls.data_source(name, key, **kwargs)
        self.search: Optional[SearchField] = None

        if 'data_type' in kwargs:

            if kwargs.get('data_type') == int:
                self.data_type = 'integer'

            if kwargs.get('data_type') == float:
                self.data_type = 'float'

        if 'auto_search' in kwargs and kwargs.get('auto_search'):
            if self.data_type:
                self.search = SearchField.set(name=name, key=key, data_type=self.data_type)
            else:
                self.search = SearchField.set(name=name, key=key)

    def __eq__(self, name: str):
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
    def _create_cst_meta(field_cls: BaseDynamicField, name: str, key: str, **kwargs) -> CSTMeta:
        return CSTMeta(field_cls, name, key, **kwargs)

    def _get_cst_field_index(self, name: str) -> int:
        return self.cst_meta_list.index(name)

    def insert_cst_meta_field(self, previous_field_name: str, field_cls: BaseDynamicField, name: str, key: str,
                              **kwargs) -> None:

        cst_meta = self._create_cst_meta(field_cls, name, key, **kwargs)
        previous_field_index = self._get_cst_field_index(previous_field_name)
        self.cst_meta_list.insert(previous_field_index + 1, cst_meta)

    def append_cst_meta_field(self, field_cls: BaseDynamicField, name: str, key: str, **kwargs) -> None:

        cst_meta = self._create_cst_meta(field_cls, name, key, **kwargs)
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

            if kwargs.get("ignore_associated_resource"):
                if cst_meta.kwargs.get('associated_resource'):
                    continue

            key = cst_meta.key
            field_cls = cst_meta.field_cls

            if kwargs.get("ignore_root_path"):
                splited_key = key.split(".")

                try:
                    splited_key.remove(kwargs.get("ignore_root_path"))
                    key = ".".join(splited_key)
                except ValueError:
                    pass

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
