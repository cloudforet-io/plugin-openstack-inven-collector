from schematics.types import ModelType, ListType, StringType, IntType, DateTimeType, DictType, \
    IPAddressType

from spaceone.inventory.model.resources.base import ResourceModel


class NicModel(ResourceModel):
    network_name = StringType()
    mac_addr = StringType(serialize_when_none=False)
    type = StringType()
    addr = IPAddressType()
    version = IntType()


class FlavorModel(ResourceModel):
    name = StringType()
    original_name = StringType(serialize_when_none=False)
    disk = IntType()
    ephemeral = IntType(default=0)
    ram = IntType()
    swap = IntType(default=0)
    vcpus = IntType()
    extra_specs = DictType(StringType)


class InstanceModel(ResourceModel):
    id = StringType()
    name = StringType()
    description = StringType()
    instance_name = StringType()
    availability_zone = StringType()
    access_ip_v4 = IPAddressType()
    access_ip_v6 = IPAddressType()
    hypervisor_id = StringType(default=None)
    hypervisor_name = StringType(default=None)
    host_status = StringType()
    key_name = StringType()
    project_name = StringType()
    root_device_name = StringType()
    server_groups = StringType(default=None)
    user_data = StringType(default=None)
    user_id = StringType()
    status = StringType()
    attached_volumes = ListType(StringType, default=[])
    created_at = DateTimeType()
    updated_at = DateTimeType()
    launched_at = DateTimeType()
    image_name = StringType()
    security_groups = ListType(ModelType('SecurityGroupModel'), default=[])
    security_group_rules = ListType(ModelType('SecurityGroupRuleModel'), default=[])
    addresses = ListType(ModelType(NicModel, serialize_when_none=False))
    flavor = ModelType(FlavorModel, serialize_when_none=False)
    volumes = ListType(ModelType('VolumeModel'), default=[])
