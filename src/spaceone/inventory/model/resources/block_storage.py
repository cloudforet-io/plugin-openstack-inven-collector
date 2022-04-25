from spaceone.inventory.model.resources.base import ResourceModel
from spaceone.inventory.model.common.base import ReferenceModel
from schematics.types import ModelType, ListType, StringType, IntType, DateTimeType, BooleanType, FloatType, DictType


class VolumeModel(ResourceModel):
    id = StringType()
    image_id = StringType()
    name = StringType()
    multiattach = BooleanType(default=False)
    size = IntType()
    volume_type = StringType()
    description = StringType()
    availability_zone = StringType()
    is_bootable = BooleanType(default=None)
    is_encrypted = BooleanType(default=None)
    project_id = StringType()
    snapshot_id = StringType()
    source_volume_id = StringType()
    host = StringType()
    status = StringType()
    attachments = ListType(StringType, default=[])
    volume_image_metadata = DictType(StringType, serialize_when_none=False)
    created_at = DateTimeType()
    launched_at = DateTimeType()
    reference = ModelType(ReferenceModel, serialize_when_none=False)
