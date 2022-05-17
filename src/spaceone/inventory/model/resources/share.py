from schematics.types import ListType, StringType, IntType, DateTimeType, BooleanType, FloatType

from spaceone.inventory.model.resources.base import ResourceModel


class ShareModel(ResourceModel):

    name = StringType()
    description = StringType()
    size = FloatType(default=0)
    size_gb = IntType(default=0)
    availability_zone = StringType()
    snapshot_id = StringType()
    source_volume_id = StringType()
    export_location = StringType()
    export_locations = ListType(StringType, default=[])
    share_type = StringType()
    share_proto = StringType()
    share_network_id = StringType()
    share_server_id = StringType()
    volume_type = StringType()
    host = StringType()
    is_public = BooleanType()
    status = StringType()
    created_at = DateTimeType()
