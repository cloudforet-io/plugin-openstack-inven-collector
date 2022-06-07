from schematics.types import ModelType, ListType, StringType, IntType, DateTimeType, DictType, \
    IPAddressType, FloatType

from spaceone.inventory.model.resources.base import ResourceModel


class NicModel(ResourceModel):
    network_name = StringType()
    mac_addr = StringType(serialize_when_none=False)
    type = StringType()
    addr = IPAddressType()
    version = IntType()


class InstanceModel(ResourceModel):
    id = StringType()
    name = StringType()
    description = StringType()
    instance_name = StringType()
    availability_zone = StringType()
    access_ip_v4 = IPAddressType()
    access_ip_v6 = IPAddressType()
    hostname = StringType()
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
    vm_state = StringType()
    attached_volumes = ListType(StringType, default=[])
    created_at = DateTimeType()
    updated_at = DateTimeType()
    launched_at = DateTimeType()
    image_name = StringType()
    image_id = StringType()
    metadata = DictType(StringType, default={})
    security_groups = ListType(ModelType('SecurityGroupModel'), default=[])
    security_group_rules = ListType(ModelType('SecurityGroupRuleModel'), default=[])
    addresses = ListType(ModelType(NicModel, serialize_when_none=False))
    flavor = DictType(StringType, default={}, serialize_when_none=False)
    volumes = ListType(ModelType('VolumeModel'), default=[])
    volume_count = IntType(serialize_when_none=False)
    total_volume_size = FloatType(serialize_when_none=False)


class ComputeQuotaModel(ResourceModel):

    quota_type = StringType(default="Compute")
    cores = DictType(StringType, serialize_when_none=False)
    fixed_ips = DictType(StringType, serialize_when_none=False)
    floating_ips = DictType(StringType, serialize_when_none=False)
    injected_file_content_bytes = DictType(StringType, serialize_when_none=False)
    injected_file_path_bytes = DictType(StringType, serialize_when_none=False)
    injected_files = DictType(StringType, serialize_when_none=False)
    instances = DictType(StringType, serialize_when_none=False)
    key_pairs = DictType(StringType, serialize_when_none=False)
    metadata_items = DictType(StringType, serialize_when_none=False)
    networks = DictType(StringType, serialize_when_none=False)
    ram = DictType(StringType, serialize_when_none=False)
    security_group_rules = DictType(StringType, serialize_when_none=False)
    security_groups = DictType(StringType, serialize_when_none=False)
    server_group_members = DictType(StringType, serialize_when_none=False)
    server_groups = DictType(StringType, serialize_when_none=False)


class ComputeAZModel(ResourceModel):

    name = StringType()
    hosts = DictType(StringType, default=None)
    state = DictType(StringType, serialize_when_none=False)
    total_memory_size = IntType()
    total_memory_used = IntType()
    total_memory_free = IntType()
    total_running_vms = IntType()
    total_vcpus = IntType()
    total_vcpus_used = IntType()
    total_vcpus_free = IntType()
    hypervisors = ListType(ModelType('HypervisorModel', default=[]))


class ServerGroupModel(ResourceModel):

    name = StringType()
    member_ids = ListType(StringType, default=None)
    metadata = DictType(StringType, serialize_when_none=False)
    policy = StringType()
    policies = ListType(StringType, default=None)
    user_id = StringType()
    rules = DictType(StringType, serialize_when_none=False)
    member_count = IntType()
    instances = ListType(ModelType(InstanceModel), serialize_when_none=False)

