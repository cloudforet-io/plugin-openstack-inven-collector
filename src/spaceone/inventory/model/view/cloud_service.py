from schematics import Model
from schematics.types import ListType, StringType, PolyModelType, DictType, ModelType, FloatType

from .base import BaseMetaData, BaseResponse, MetaDataView, MetaDataViewSubData, ReferenceModel

class Labels(Model):
    key = StringType()
    value = StringType()


class CloudServiceMeta(BaseMetaData):
    @classmethod
    def set(cls):
        sub_data = MetaDataViewSubData()
        return cls({'view': MetaDataView({'sub_data': sub_data})})

    @classmethod
    def set_layouts(cls, layouts=[]):
        sub_data = MetaDataViewSubData({'layouts': layouts})
        return cls({'view': MetaDataView({'sub_data': sub_data})})


'''
Check
Compute 플러그인에서 서버의 Metadata는 별도로 리턴 하는것 같아서 여기로 통합함
'''


class ServerMetadata(Model):
    view = ModelType(MetaDataView)

    @classmethod
    def set_layouts(cls, layouts=[]):
        sub_data = MetaDataViewSubData({'layouts': layouts})
        return cls({'view': MetaDataView({'sub_data': sub_data})})