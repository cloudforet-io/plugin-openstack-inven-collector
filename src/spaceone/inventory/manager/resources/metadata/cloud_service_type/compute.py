import os

from spaceone.inventory.model.view.dynamic_widget import ChartWidget, CardWidget
from spaceone.inventory.model.view.dynamic_field import TextDyField,DateTimeDyField, ListDyField
from spaceone.inventory.model.common.response import CloudServiceTypeResource
from spaceone.inventory.model.view.cloud_service_type import CloudServiceTypeMeta
from spaceone.inventory.libs.common_parser import get_data_from_yaml
from spaceone.inventory.libs.metaman import CSTMetaGenerator

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/compute/total_count.yml')
count_by_account_conf = os.path.join(current_dir, 'widget/compute/count_by_account.yml')
count_by_flavor_conf = os.path.join(current_dir, 'widget/compute/count_by_flavor.yml')

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

CST_INSTANCE_META.set_cst_meta_field(TextDyField, 'Name', 'data.name')
CST_INSTANCE_META.set_cst_meta_field(TextDyField, 'ID', 'data.id')
CST_INSTANCE_META.set_cst_meta_field(TextDyField, 'Status', 'data.status', default_state={
                                    'safe': ['ACTIVE'],
                                    'available': ['BUILD', 'PAUSED'],
                                    'warning': ['MIGRATING', 'HARD_REBOOT', 'PASSWORD', 'REBOOT', 'REBUILD', 'RESCUE'],
                                    'disable': ['DELETED', 'SUSPENDED', 'SHUTOFF'],
                                    'alert': ['ERROR']}
                                     )
CST_INSTANCE_META.set_cst_meta_field(TextDyField, 'Flavor', 'data.flavor.name')
CST_INSTANCE_META.set_cst_meta_field(TextDyField, 'IP Address', 'data.minimal_addresses')
CST_INSTANCE_META.set_cst_meta_field(TextDyField, 'Key Name', 'data.key_name')
CST_INSTANCE_META.set_cst_meta_field(TextDyField, 'Availability Zone', 'data.availability_zone')
CST_INSTANCE_META.set_cst_meta_field(ListDyField, 'Security Groups', 'data.security_groups')
CST_INSTANCE_META.set_cst_meta_field(TextDyField, 'Image Name', 'data.image_name')
CST_INSTANCE_META.set_cst_meta_field(ListDyField, 'Volumes', 'data.volumes.id',
                                     reference={"resource_type": "inventory.CloudService",
                                                "reference_key": "reference.resource_id"})
CST_INSTANCE_META.set_cst_meta_field(DateTimeDyField, 'Created', 'data.created_at')
CST_INSTANCE_META.set_cst_meta_field(DateTimeDyField, 'Updated', 'data.updated_at', options={'is_optional': True})

CLOUD_SERVICE_TYPE._metadata = CloudServiceTypeMeta.set_meta(fields=CST_INSTANCE_META.fields,
                                                             search=CST_INSTANCE_META.search,
                                                             widget=[
                                                                 CardWidget.set(**get_data_from_yaml(total_count_conf)),
                                                                 ChartWidget.set(
                                                                     **get_data_from_yaml(count_by_account_conf)),

                                                                 ChartWidget.set(
                                                                     **get_data_from_yaml(count_by_flavor_conf)),
                                                             ]
                                                             )
