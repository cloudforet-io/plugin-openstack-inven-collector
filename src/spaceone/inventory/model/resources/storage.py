from schematics.types import ListType, StringType, IntType, DateTimeType, BooleanType, FloatType, DictType

from spaceone.inventory.model.resources.base import ResourceModel


class StorageModel(ResourceModel):

    display_name = StringType()
    namespace = StringType()
    pool_name = StringType()
    description = StringType()
    driver_version = StringType()
    properties = DictType(StringType, serialize_when_none=False)
    replication_targets = ListType(StringType, serialize_when_none=False)
    storage_protocol = StringType()
    vendor_name = StringType()
    visibility = StringType()
    volume_backend_name = StringType()
    total_allocated_volume_size = FloatType()
    total_volume_count = IntType()
    attached_volume_count = IntType()
    available_volume_count = IntType()


