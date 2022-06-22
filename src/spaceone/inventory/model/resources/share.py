from schematics.types import ListType, StringType, IntType, DateTimeType, BooleanType, FloatType, DictType, ModelType

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
    share_protocol = StringType()
    share_network = ModelType('ShareNetworkModel')
    share_network_id = StringType()
    share_server_id = StringType()
    volume_type = StringType()
    host = StringType()
    is_public = BooleanType()
    status = StringType()
    created_at = DateTimeType()


class ShareNetworkModel(ResourceModel):
    name = StringType()
    description = StringType()
    neutron_net_id = StringType()
    neutron_subnet_id = StringType()
    network_type = StringType()
    segmentation_id = IntType()
    cidr = StringType()
    ip_version = StringType()
    name = StringType()
    description = StringType()
    created_at = DateTimeType()
    updated_at = DateTimeType()
    gateway = StringType()
    mtu = StringType()
    share_network_subnets = ListType(DictType(StringType), default=[])
    security_service_update_support = BooleanType()
    status = StringType()
