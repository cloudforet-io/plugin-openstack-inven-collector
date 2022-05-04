from schematics import Model
from schematics.types import ListType, StringType, PolyModelType, DictType, ModelType, BooleanType, DateTimeType, FloatType

class ReferenceModel(Model):
    class Option:
        serialize_when_none = False

    bookmark_link = StringType()
    self_link = StringType()

class ResourceModel(Model):
    id = StringType(default=None, serialize_when_none=False)
    reference = ModelType(ReferenceModel, serialize_when_none=False)
    external_link = StringType()
    region_name = StringType()


