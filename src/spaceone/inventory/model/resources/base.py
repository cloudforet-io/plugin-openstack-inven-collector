from schematics import Model
from schematics.types import ListType, StringType, PolyModelType, DictType, ModelType, BooleanType, DateTimeType, FloatType

class ResourceModel(Model):
    id = StringType(default=None, serialize_when_none=False)
    reference = ModelType("ReferenceModel")

class ReferenceModel(Model):
    class Option:
        serialize_when_none = False

    bookmark_link = StringType(required=False, serialize_when_none=False)
    self_link = StringType(required=False, serialize_when_none=False)


