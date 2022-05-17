from schematics import Model
from schematics.types import ListType, StringType, PolyModelType, DictType, ModelType, FloatType, BooleanType

from spaceone.inventory.model.view.cloud_service import CloudServiceMeta
from spaceone.inventory.model.view.cloud_service_type import CloudServiceTypeMeta


class Labels(Model):
    key = StringType()
    value = StringType()


class CloudServiceReferenceModel(Model):
    class Option:
        serialize_when_none = False

    resource_id = StringType(required=False, serialize_when_none=False)
    external_link = StringType(required=False, serialize_when_none=False)


class CloudServiceResource(Model):
    provider = StringType(default="openstack")
    account = StringType()
    instance_type = StringType(serialize_when_none=False)
    instance_size = FloatType(serialize_when_none=False)
    launched_at = StringType(serialize_when_none=False)
    cloud_service_type = StringType()
    cloud_service_group = StringType()
    name = StringType(default="")
    project_id = StringType()
    region_code = StringType()
    data = PolyModelType(Model, default=lambda: {})
    tags = ListType(ModelType(Labels), serialize_when_none=False)
    reference = ModelType(CloudServiceReferenceModel)
    _metadata = PolyModelType(CloudServiceMeta, serialize_when_none=False, serialized_name='metadata')


class CloudServiceTypeResource(Model):
    name = StringType()
    provider = StringType()
    group = StringType()
    _metadata = PolyModelType(CloudServiceTypeMeta, serialize_when_none=False, serialized_name='metadata')
    labels = ListType(StringType(), serialize_when_none=False)
    tags = DictType(StringType, serialize_when_none=False)
    is_primary = BooleanType(default=False)
    is_major = BooleanType(default=False)
    resource_type = StringType(default='inventory.CloudService')
    service_code = StringType(serialize_when_none=False)


class ErrorResource(Model):
    resource_type = StringType(default='inventory.CloudService')
    provider = StringType(default="openstack")
    cloud_service_group = StringType(default='', serialize_when_none=False)
    cloud_service_type = StringType(default='', serialize_when_none=False)
    resource_id = StringType(serialize_when_none=False)
