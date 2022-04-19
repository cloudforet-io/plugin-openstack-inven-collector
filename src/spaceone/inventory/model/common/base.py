from schematics import Model
from spaceone.inventory.model.common.region import RegionModel
from spaceone.inventory.model import ResourceModel
from schematics.types import ListType, StringType, PolyModelType, DictType, ModelType, FloatType


class Labels(Model):
    key = StringType()
    value = StringType()


class ReferenceModel(Model):
    class Option:
        serialize_when_none = False
    bookmark_link = StringType(required=False, serialize_when_none=False)
    self_link = StringType(required=False, serialize_when_none=False)


class CloudServiceResource(Model):
    provider = StringType(default="openstack")
    account = StringType()
    instance_type = StringType(serialize_when_none=False)
    instance_size = FloatType(serialize_when_none=False)
    launched_at = StringType(serialize_when_none=False)
    cloud_service_type = StringType()
    cloud_service_group = StringType()
    name = StringType(default="")
    region_code = StringType()
    tags = ListType(ModelType(Labels), serialize_when_none=False)
    reference = ModelType(ReferenceModel)

