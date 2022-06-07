import os

from spaceone.inventory.libs.common_parser import get_data_from_yaml
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.common.response import CloudServiceTypeResource
from spaceone.inventory.model.view.cloud_service_type import CloudServiceTypeMeta
from spaceone.inventory.model.view.dynamic_field import TextDyField, EnumDyField
from spaceone.inventory.model.view.dynamic_widget import ChartWidget, CardWidget

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/availability_zone/total_count.yml')
count_by_region_conf = os.path.join(current_dir, 'widget/availability_zone/count_by_region.yml')

CLOUD_SERVICE_TYPE = CloudServiceTypeResource()
CLOUD_SERVICE_TYPE.provider = 'openstack'
CLOUD_SERVICE_TYPE.name = 'Availability Zone'
CLOUD_SERVICE_TYPE.group = 'Compute'
CLOUD_SERVICE_TYPE.labels = ['Compute', 'Availability Zone']
CLOUD_SERVICE_TYPE.is_primary = False
CLOUD_SERVICE_TYPE.is_major = False
CLOUD_SERVICE_TYPE.service_code = 'OSComputeAZ'
CLOUD_SERVICE_TYPE.tags = {
    'spaceone:icon': 'https://wiki.openstack.org/w/images/2/2c/Nova-complete-300.svg',
    'spaceone:display_name': 'ComputeAZ'
}

CST_COMPUTE_ZONE_META = CSTMetaGenerator()

CST_COMPUTE_ZONE_META.append_cst_meta_field(TextDyField, 'Name', 'data.name', auto_search=True)
CST_COMPUTE_ZONE_META.append_cst_meta_field(TextDyField, 'Instances', 'data.total_running_vms', auto_search=True,
                                            data_type=int)
CST_COMPUTE_ZONE_META.append_cst_meta_field(TextDyField, 'vCPU(total)', 'data.total_vcpus', auto_search=True,
                                            data_type=int)
CST_COMPUTE_ZONE_META.append_cst_meta_field(TextDyField, 'vCPU(used)', 'data.total_vcpus_used', auto_search=True,
                                            data_type=int)
CST_COMPUTE_ZONE_META.append_cst_meta_field(TextDyField, 'vCPU(free)', 'data.total_vcpus_free', auto_search=True,
                                            data_type=int)
CST_COMPUTE_ZONE_META.append_cst_meta_field(TextDyField, 'MEM(total)', 'data.total_memory_size', auto_search=True,
                                            data_type=int,
                                            type="size", options={"source_unit": "MB"})
CST_COMPUTE_ZONE_META.append_cst_meta_field(TextDyField, 'MEM(used)', 'data.total_memory_used', auto_search=True,
                                            data_type=int,
                                            type="size", options={"source_unit": "MB"})
CST_COMPUTE_ZONE_META.append_cst_meta_field(TextDyField, 'MEM(free)', 'data.total_memory_free', auto_search=True,
                                            data_type=int,
                                            type="size", options={"source_unit": "MB"})
CST_COMPUTE_ZONE_META.append_cst_meta_field(EnumDyField, 'State', 'data.state.available', auto_search=True,
                                            default_badge={
                                                'indigo.500': ['true'], 'coral.600': ['false']})

CLOUD_SERVICE_TYPE._metadata = CloudServiceTypeMeta.set_meta(
    fields=CST_COMPUTE_ZONE_META.fields, search=CST_COMPUTE_ZONE_META.search,
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_region_conf)),

    ]
)
