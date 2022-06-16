from schematics.types import ListType, StringType, IntType, DateTimeType, BooleanType, FloatType, DictType

from spaceone.inventory.model.resources.base import ResourceModel


class VolumeModel(ResourceModel):
    id = StringType()
    image_id = StringType()
    name = StringType()
    description = StringType()
    multiattach = BooleanType(default=False)
    size = FloatType(default=0)
    size_gb = IntType(default=0)
    volume_type = StringType()
    availability_zone = StringType()
    is_bootable = BooleanType(default=None)
    is_encrypted = BooleanType(default=None)
    snapshot_id = StringType()
    source_volume_id = StringType()
    host = StringType()
    status = StringType()
    metadata = DictType(StringType, default={})
    attachments = ListType(StringType, default=[])
    volume_image_metadata = DictType(StringType, serialize_when_none=False)
    created_at = DateTimeType()
    launched_at = DateTimeType()


class VolumeQuotaModel(ResourceModel):
    quota_type = StringType(default="Volume")
    backup_gigabyte = FloatType()
    backups = IntType()
    gigabytes = FloatType()
    groups = IntType()
    per_volume_gigabytes = FloatType()
    snapshots = IntType()
    volumes = IntType()
    usage = DictType(StringType, serialize_when_none=False)
    reservation = DictType(StringType, serialize_when_none=False)


class SnapshotModel(ResourceModel):
    name = StringType()
    description = StringType()
    created_at = DateTimeType()
    is_forced = BooleanType(default=None)
    metadata = DictType(StringType, default={})
    size = FloatType(default=0)
    size_gb = FloatType(default=0)
    status = StringType()
    volume_id = StringType()
