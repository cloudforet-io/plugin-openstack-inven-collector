from spaceone.inventory.model.view.dynamic_field import SearchField
import copy


class CSTMetaGenerator:
    fields_list = []
    search_list = []

    def __init__(self):
        self.fields_list = []
        self.search_list = []

    def set_cst_meta_field(self, field_cls, name, key, **kwargs):
        self.fields.append(field_cls.data_source(name, key, **kwargs))

        if 'auto_search' not in kwargs or kwargs.get('auto_search'):
            self.search.append(SearchField.set(name=name, key=key))

    @property
    def fields(self):
        return self.fields_list

    @property
    def search(self):
        return self.search_list
