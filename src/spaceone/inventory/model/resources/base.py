from schematics import Model
from schematics.types import ListType, StringType, PolyModelType, DictType, ModelType, BooleanType, DateTimeType, FloatType

class ResourceModel(Model):
    reference = ModelType("ReferenceModel")


class ReferenceModel(Model):
    class Option:
        serialize_when_none = False

    resource_id = StringType(required=False, serialize_when_none=False)
    external_link = StringType(required=False, serialize_when_none=False)
