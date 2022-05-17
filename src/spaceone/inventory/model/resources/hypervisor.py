from schematics.types import StringType, IntType, DictType, IPAddressType, ListType, ModelType

from spaceone.inventory.model.resources.base import ResourceModel


class HypervisorModel(ResourceModel):
    name = StringType()
    host_ip = IPAddressType()
    hypervisor_type = StringType()
    local_disk_free = IntType()
    local_disk_size = IntType()
    local_disk_used = IntType()
    memory_free = IntType()
    memory_size = IntType()
    memory_used = IntType()
    running_vms = IntType()
    state = StringType()
    status = StringType()
    vcpus = IntType()
    vcpus_used = IntType()
    uptime = StringType()
    instances = ListType(ModelType('InstanceModel'), serialize_when_none=False)
    cpu_info = DictType(StringType, serialize_when_none=False)