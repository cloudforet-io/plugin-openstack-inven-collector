from spaceone.inventory.model.view.dynamic_layout import QuerySearchTableDynamicLayout
from .base import BaseMetaData, MetaDataViewTable, MetaDataView


class CloudServiceTypeMeta(BaseMetaData):
    @classmethod
    def set_fields(cls, name='', fields=[]):
        _table = MetaDataViewTable({'layout': QuerySearchTableDynamicLayout.set_fields(name, fields)})
        return cls({'view': MetaDataView({'table': _table})})

    @classmethod
    def set_meta(cls, name='', fields=[], search=[], widget=[]):
        table_meta = MetaDataViewTable({'layout': QuerySearchTableDynamicLayout.set_fields(name, fields)})
        return cls({'view': MetaDataView({'table': table_meta, 'search': search, 'widget': widget})})
