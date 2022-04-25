from spaceone.inventory.model.resources.base import ResourceModel
from schematics.types import ModelType, ListType, StringType, IntType, DateTimeType, BooleanType, FloatType, DictType, IPAddressType


class NetworkModel(ResourceModel):

    id = StringType()
    name = StringType()
    description = StringType()
    fixed_ip_v4 = StringType()
    fixed_ip_v6 = StringType()
    floating_ip = StringType()
    availability_zones = ListType(StringType, default=[])
    mac = StringType()
    is_port_security_enabled = BooleanType()
    is_router_external = BooleanType()
    is_shared = BooleanType()
    is_vlan_transparent = BooleanType()
    mtu = StringType()
    project_id = StringType()
    segments = ListType(DictType(StringType), default=[])
    status = StringType()
    subnet_ids = ListType(StringType, default=[])
    created_at = DateTimeType()
    updated_at = DateTimeType()

