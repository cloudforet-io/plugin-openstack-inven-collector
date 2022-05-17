from schematics.types import ModelType, ListType, StringType, IntType, DateTimeType, BooleanType, DictType, \
    IPAddressType

from spaceone.inventory.model.resources.base import ResourceModel


class NetworkModel(ResourceModel):

    id = StringType()
    name = StringType()
    description = StringType()
    fixed_ip_v4 = StringType()
    fixed_ip_v6 = StringType()
    floating_ip = StringType()
    availability_zones = ListType(StringType, default=[])
    mac = StringType()
    is_admin_state_up = BooleanType()
    is_port_security_enabled = BooleanType()
    is_router_external = BooleanType()
    is_shared = BooleanType()
    is_vlan_transparent = BooleanType(serialize_when_none=False)
    mtu = StringType()
    segments = ListType(DictType(StringType), default=[])
    status = StringType()
    created_at = DateTimeType()
    updated_at = DateTimeType()
    cidrs = ListType(StringType, default=[])
    subnets = ListType(ModelType('SubnetModel'), default=[])
    minimal_subnets = ListType(StringType(), default=[])

class SubnetModel(ResourceModel):

    id = StringType()
    name = StringType()
    description = StringType()
    allocation_pools = ListType(StringType, default=[])
    cidr = IPAddressType()
    dns_nameservers = ListType(IPAddressType, default=[])
    gateway_ip = IPAddressType()
    host_routes = ListType(IPAddressType, default=[])
    ip_version = StringType()
    is_dhcp_enabled = BooleanType()
    network_id = StringType()
    segment_id = StringType()
    created_at = DateTimeType()
    updated_at = DateTimeType()

class SegmentModel(ResourceModel):
    id = StringType()
    name = StringType()
    description = StringType()
    network_id = StringType()
    network_type = StringType()
    physical_network = StringType()
    segmentation_id = IntType()


