from schematics.types import StringType, IntType, DateTimeType, DictType, \
    FloatType, BooleanType

from spaceone.inventory.model.resources.base import ResourceModel


class ImageModel(ResourceModel):
    name = StringType()
    disk_format = StringType()
    container_format = StringType()
    hash_algo = StringType()
    checksum = StringType()
    file = StringType()
    visibility = StringType()
    is_hidden = BooleanType()
    is_protected = BooleanType()
    min_disk = IntType()
    min_ram = IntType()
    progress = IntType()
    size = FloatType()
    size_mb = FloatType()
    status = StringType()
    owner_id = StringType()
    metadata = DictType(StringType())
    properties = DictType(StringType())
    created_at = DateTimeType()
    updated_at = DateTimeType()
