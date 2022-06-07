import os

from spaceone.inventory.libs.common_parser import get_data_from_yaml
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.common.response import CloudServiceTypeResource
from spaceone.inventory.model.view.cloud_service_type import CloudServiceTypeMeta
from spaceone.inventory.model.view.dynamic_field import TextDyField, DateTimeDyField, ListDyField, EnumDyField, \
    BadgeDyField
from spaceone.inventory.model.view.dynamic_widget import ChartWidget, CardWidget

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/compute/total_count.yml')
total_vcpu_count_conf = os.path.join(current_dir, 'widget/compute/total_vcpu_count.yml')
total_memory_size_conf = os.path.join(current_dir, 'widget/compute/total_memory_size.yml')
total_volume_size_conf = os.path.join(current_dir, 'widget/compute/total_volume_size.yml')
total_vcpu_count_by_project_conf = os.path.join(current_dir, 'widget/compute/total_vcpu_count_by_project.yml')
total_memory_size_by_project_conf = os.path.join(current_dir, 'widget/compute/total_memory_size_by_project.yml')
total_volume_size_by_project_conf = os.path.join(current_dir, 'widget/compute/total_volume_size_by_project.yml')
count_by_project_conf = os.path.join(current_dir, 'widget/compute/count_by_project.yml')
count_by_flavor_conf = os.path.join(current_dir, 'widget/compute/count_by_flavor.yml')
count_by_region_conf = os.path.join(current_dir, 'widget/compute/count_by_region.yml')

CLOUD_SERVICE_TYPE = CloudServiceTypeResource()
CLOUD_SERVICE_TYPE.provider = 'openstack'
CLOUD_SERVICE_TYPE.name = 'Instance'
CLOUD_SERVICE_TYPE.group = 'Compute'
CLOUD_SERVICE_TYPE.labels = ['Compute', 'Server']
CLOUD_SERVICE_TYPE.is_primary = True
CLOUD_SERVICE_TYPE.is_major = True
CLOUD_SERVICE_TYPE.service_code = 'OSCompute'
CLOUD_SERVICE_TYPE.tags = {
    'spaceone:icon': 'https://wiki.openstack.org/w/images/2/2c/Nova-complete-300.svg',
    'spaceone:display_name': 'Instance'
}

CST_INSTANCE_META = CSTMetaGenerator()

CST_INSTANCE_META.append_cst_meta_field(TextDyField, 'Name', 'data.name')
CST_INSTANCE_META.append_cst_meta_field(BadgeDyField, 'ID', 'data.id', auto_search=True,
                                        reference={"resource_type": "inventory.CloudService",
                                                   "reference_key": "reference.resource_id"},
                                        options={'is_optional': True})
CST_INSTANCE_META.append_cst_meta_field(TextDyField, 'Host Name', 'data.hostname', auto_search=True,
                                        options={'is_optional': True})
CST_INSTANCE_META.append_cst_meta_field(EnumDyField, 'Status', 'data.status', auto_search=True,
                                        default_state={
                                            'safe': ['ACTIVE'],
                                            'available': ['BUILD', 'PAUSED'],
                                            'warning': ['HARD_REBOOT', 'MIGRATING', 'PASSWORD', 'REBOOT', 'REBUILD',
                                                        'RESCUE', 'RESIZE', 'REVERT_RESIZE', 'SHELVED',
                                                        'VERIFY_RESIZE'],
                                            'disable': ['SOFT_DELETED', 'PAUSED', 'DELETED', 'SUSPENDED', 'SHUTOFF'],
                                            'alert': ['ERROR', 'UNKNOWN']}
                                        )
CST_INSTANCE_META.append_cst_meta_field(EnumDyField, 'VM State', 'data.vm_state', auto_search=True,
                                        default_state={
                                            'safe': ['ACTIVE'],
                                            'available': ['BUILD', 'RESCUED', 'RESIZED', 'SHELVED',
                                                          'SHELVED_OFFLOADED'],
                                            'warning': ['BUILDING'],
                                            'disable': ['DELETED', 'PAUSED', 'SOFT_DELETED', 'STOPPED', 'SUSPENDED'],
                                            'alert': ['ERROR']}
                                        )
CST_INSTANCE_META.append_cst_meta_field(TextDyField, 'Flavor', 'data.flavor.name', auto_search=True)
CST_INSTANCE_META.append_cst_meta_field(TextDyField, 'vCPU', 'data.flavor.vcpus', auto_search=True, data_type=int)
CST_INSTANCE_META.append_cst_meta_field(TextDyField, 'Memory', 'data.flavor.ram', auto_search=True, data_type=int,
                                        type="size", options={"source_unit": "MB"})
CST_INSTANCE_META.append_cst_meta_field(TextDyField, 'Volume Size', 'data.total_volume_size', auto_search=True,
                                        data_type=int,
                                        type="size", options={"source_unit": "GB", "display_unit": "GB"}
                                        )
CST_INSTANCE_META.append_cst_meta_field(TextDyField, 'Volume Count', 'data.volume_count', auto_search=True,
                                        data_type=int)
CST_INSTANCE_META.append_cst_meta_field(ListDyField, 'IP Address', 'data.addresses', auto_search=True,
                                        options={'delimiter': ', ', 'sub_key': 'addr'})
CST_INSTANCE_META.append_cst_meta_field(TextDyField, 'Key Name', 'data.key_name', auto_search=True)
CST_INSTANCE_META.append_cst_meta_field(TextDyField, 'Availability Zone', 'data.availability_zone', auto_search=True)
CST_INSTANCE_META.append_cst_meta_field(ListDyField, 'Security Groups', 'data.security_groups', auto_search=True,
                                        options={'delimiter': ', ', 'sub_key': 'name'})
CST_INSTANCE_META.append_cst_meta_field(TextDyField, 'Image Name', 'data.image_name', auto_search=True,
                                        associated_resource=True)
CST_INSTANCE_META.append_cst_meta_field(BadgeDyField, 'Image ID', 'data.image_id',
                                        reference={"resource_type": "inventory.CloudService",
                                                   "reference_key": "reference.resource_id"},
                                        options={'is_optional': True}
                                        )
CST_INSTANCE_META.append_cst_meta_field(TextDyField, 'Hypervisor Name', 'data.hypervisor_name', auto_search=True)
CST_INSTANCE_META.append_cst_meta_field(BadgeDyField, 'Hypervisor ID', 'data.hypervisor_id', auto_search=True,
                                        reference={"resource_type": "inventory.CloudService",
                                                   "reference_key": "reference.resource_id"},
                                        options={'is_optional': True}
                                        )
CST_INSTANCE_META.append_cst_meta_field(TextDyField, 'Instance Name', 'data.instance_name', auto_search=True,
                                        options={'is_optional': True})
CST_INSTANCE_META.append_cst_meta_field(ListDyField, 'Volumes', 'data.volumes', auto_search=True,
                                        reference={"resource_type": "inventory.CloudService",
                                                   "reference_key": "reference.resource_id"},
                                        default_badge={"type": "reference", 'delimiter': ' ', 'sub_key': 'id'},
                                        options={'is_optional': True}
                                        )
CST_INSTANCE_META.append_cst_meta_field(ListDyField, 'Networks', 'data.addresses', auto_search=True,
                                        options={'delimiter': ', ', 'sub_key': 'network_name'}
                                        )
CST_INSTANCE_META.append_cst_meta_field(TextDyField, 'Project Name', 'data.project_name', auto_search=True)
CST_INSTANCE_META.append_cst_meta_field(BadgeDyField, 'Project ID', 'data.project_id', auto_search=True,
                                        reference={"resource_type": "inventory.CloudService",
                                                   "reference_key": "reference.resource_id"},
                                        options={'is_optional': True})
CST_INSTANCE_META.append_cst_meta_field(BadgeDyField, 'User ID', 'data.user_id', auto_search=True,
                                        reference={"resource_type": "inventory.CloudService",
                                                   "reference_key": "reference.resource_id"},
                                        options={'is_optional': True})
CST_INSTANCE_META.append_cst_meta_field(DateTimeDyField, 'Created', 'data.created_at', auto_search=True)
CST_INSTANCE_META.append_cst_meta_field(DateTimeDyField, 'Updated', 'data.updated_at', auto_search=True,
                                        options={'is_optional': True})

CLOUD_SERVICE_TYPE._metadata = CloudServiceTypeMeta.set_meta(fields=CST_INSTANCE_META.fields,
                                                             search=CST_INSTANCE_META.search,
                                                             widget=[
                                                                 CardWidget.set(**get_data_from_yaml(total_count_conf)),
                                                                 CardWidget.set(
                                                                     **get_data_from_yaml(total_vcpu_count_conf)),
                                                                 CardWidget.set(
                                                                     **get_data_from_yaml(total_memory_size_conf)),
                                                                 CardWidget.set(
                                                                     **get_data_from_yaml(total_volume_size_conf)),
                                                                 ChartWidget.set(
                                                                     **get_data_from_yaml(count_by_project_conf)),
                                                                 ChartWidget.set(
                                                                     **get_data_from_yaml(count_by_flavor_conf)),
                                                                 ChartWidget.set(
                                                                     **get_data_from_yaml(count_by_region_conf)),
                                                                 ChartWidget.set(
                                                                     **get_data_from_yaml(
                                                                         total_vcpu_count_by_project_conf)),
                                                                 ChartWidget.set(
                                                                     **get_data_from_yaml(
                                                                         total_memory_size_by_project_conf)),
                                                                 ChartWidget.set(
                                                                     **get_data_from_yaml(
                                                                         total_volume_size_by_project_conf)),
                                                             ]
                                                             )
