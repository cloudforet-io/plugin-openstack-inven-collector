import os

from spaceone.inventory.libs.common_parser import get_data_from_yaml
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.common.response import CloudServiceTypeResource
from spaceone.inventory.model.view.cloud_service_type import CloudServiceTypeMeta
from spaceone.inventory.model.view.dynamic_field import TextDyField, EnumDyField, BadgeDyField
from spaceone.inventory.model.view.dynamic_widget import ChartWidget, CardWidget

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/hypervisor/total_count.yml')
total_vcpu_count_conf = os.path.join(current_dir, 'widget/hypervisor/total_vcpu_count.yml')
total_memory_count_conf = os.path.join(current_dir, 'widget/hypervisor/total_memory_count.yml')
used_vcpu_count_conf = os.path.join(current_dir, 'widget/hypervisor/used_vcpu_count.yml')
used_memory_count_conf = os.path.join(current_dir, 'widget/hypervisor/used_memory_count.yml')
count_by_region_conf = os.path.join(current_dir, 'widget/hypervisor/count_by_region.yml')
usage_memory_size_conf = os.path.join(current_dir, 'widget/hypervisor/usage_memory.yml')

CLOUD_SERVICE_TYPE = CloudServiceTypeResource()
CLOUD_SERVICE_TYPE.provider = 'openstack'
CLOUD_SERVICE_TYPE.name = 'Hypervisor'
CLOUD_SERVICE_TYPE.group = 'Compute'
CLOUD_SERVICE_TYPE.labels = ['Compute', 'Hypervisor']
CLOUD_SERVICE_TYPE.is_primary = True
CLOUD_SERVICE_TYPE.is_major = True
CLOUD_SERVICE_TYPE.service_code = 'OSHypervisor'
CLOUD_SERVICE_TYPE.tags = {
    'spaceone:icon': 'https://wiki.openstack.org/w/images/2/2c/Nova-complete-300.svg',
    'spaceone:display_name': 'Hypervisor'
}

CST_HV_META = CSTMetaGenerator()

CST_HV_META.append_cst_meta_field(TextDyField, 'Name', 'data.name')
CST_HV_META.append_cst_meta_field(BadgeDyField, 'ID', 'data.id', auto_search=True,
                                  reference={"resource_type": "inventory.CloudService",
                                             "reference_key": "reference.resource_id"},
                                  options={'is_optional': True})
CST_HV_META.append_cst_meta_field(TextDyField, 'Instances Count', 'data.running_vms', auto_search=True)
CST_HV_META.append_cst_meta_field(EnumDyField, 'State', 'data.state', auto_search=True,
                                  default_badge={
                                      'green.500': ['UP'], 'red.500': ['DOWN']
                                  })
CST_HV_META.append_cst_meta_field(EnumDyField, 'Status', 'data.status', auto_search=True,
                                  default_badge={
                                      'green.500': ['ENABLED'], 'gray.500': ['DISABLED']
                                  })
CST_HV_META.append_cst_meta_field(TextDyField, 'IP Address', 'data.host_ip', auto_search=True)
CST_HV_META.append_cst_meta_field(TextDyField, 'Type', 'data.hypervisor_type', auto_search=True)

CST_HV_META.append_cst_meta_field(TextDyField, 'vCPU(total)', 'data.vcpus', auto_search=True, data_type=int)
CST_HV_META.append_cst_meta_field(TextDyField, 'vCPU(used)', 'data.vcpus_used', auto_search=True, data_type=int)
CST_HV_META.append_cst_meta_field(TextDyField, 'vCPU Model', 'data.cpu_info.model', auto_search=True)
CST_HV_META.append_cst_meta_field(TextDyField, 'vCPU Topology', 'data.cpu_info.topology', auto_search=True,
                                  options={'is_optional': True})
CST_HV_META.append_cst_meta_field(TextDyField, 'Memory(total)', 'data.memory_size', auto_search=True,  data_type=int,
                                  type="size", options={"source_unit": "MB"})
CST_HV_META.append_cst_meta_field(TextDyField, 'Memory(used)', 'data.memory_used', auto_search=True,  data_type=int,
                                  type="size", options={"source_unit": "MB"})
CST_HV_META.append_cst_meta_field(TextDyField, 'Memory(free)', 'data.memory_free', auto_search=True,  data_type=int,
                                  type="size", options={"source_unit": "MB", 'is_optional': True})
CST_HV_META.append_cst_meta_field(TextDyField, 'Local Storage(total)', 'data.local_disk_size', auto_search=True, data_type=int,
                                  type="size", options={"source_unit": "GB"})
CST_HV_META.append_cst_meta_field(TextDyField, 'Local Storage(used)', 'data.local_disk_used', auto_search=True, data_type=int,
                                  type="size", options={"source_unit": "GB", "display_unit": "GB"})
CST_HV_META.append_cst_meta_field(TextDyField, 'Local Storage(free)', 'data.local_disk_free', auto_search=True,  data_type=int,
                                  type="size", options={"source_unit": "GB", "display_unit": "GB", 'is_optional': True})
CST_HV_META.append_cst_meta_field(TextDyField, 'Availability Zone', 'data.availability_zone', auto_search=True)
CST_HV_META.append_cst_meta_field(TextDyField, 'Uptime', 'data.uptime', auto_search=True,
                                  options={'is_optional': True})

CLOUD_SERVICE_TYPE._metadata = CloudServiceTypeMeta.set_meta(
    fields=CST_HV_META.fields, search=CST_HV_META.search,
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        CardWidget.set(**get_data_from_yaml(total_vcpu_count_conf)),
        CardWidget.set(**get_data_from_yaml(used_vcpu_count_conf)),
        CardWidget.set(**get_data_from_yaml(total_memory_count_conf)),
        CardWidget.set(**get_data_from_yaml(used_memory_count_conf)),
        ChartWidget.set(
            **get_data_from_yaml(count_by_region_conf)),
        ChartWidget.set(
            **get_data_from_yaml(usage_memory_size_conf))]
)
