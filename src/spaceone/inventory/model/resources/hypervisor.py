from schematics.types import StringType, IntType, DictType, IPAddressType, ListType, ModelType, FloatType

from spaceone.inventory.model.resources.base import ResourceModel
from spaceone.inventory.model.resources.compute import InstanceModel


class HypervisorModel(ResourceModel):
    name = StringType()
    host_ip = IPAddressType()
    hypervisor_type = StringType()
    local_disk_free = FloatType(default=0)
    local_disk_size = FloatType(default=0)
    local_disk_used = FloatType(default=0)
    local_disk_allocation_ratio = IntType(default=1)
    memory_free = FloatType(default=0)
    memory_size = FloatType(default=0)
    memory_used = FloatType(default=0)
    memory_allocation_ratio = IntType(default=1)
    running_vms = IntType(default=0)
    state = StringType()
    status = StringType()
    vcpus = IntType(default=0)
    vcpus_used = IntType(default=0)
    vcpus_free = IntType(default=0)
    vcpus_allocation_ratio = IntType(default=1)
    uptime = StringType()
    instances = ListType(ModelType(InstanceModel), serialize_when_none=False)
    cpu_info = DictType(StringType, serialize_when_none=False)
    availability_zone = StringType(serialize_when_none=False)