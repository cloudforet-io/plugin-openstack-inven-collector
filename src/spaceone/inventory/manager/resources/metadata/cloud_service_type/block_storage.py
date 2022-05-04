import os
from spaceone.inventory.model.view.dynamic_widget import ChartWidget, CardWidget
from spaceone.inventory.model.view.dynamic_field import TextDyField, EnumDyField, SearchField, DateTimeDyField
from spaceone.inventory.model.common.response import CloudServiceTypeResource
from spaceone.inventory.model.view.cloud_service_type import CloudServiceTypeMeta
from spaceone.inventory.libs.common_parser import get_data_from_yaml
from spaceone.inventory.libs.metaman import CSTMetaGenerator

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/compute/total_count.yml')

CLOUD_SERVICE_TYPE = CloudServiceTypeResource()
CLOUD_SERVICE_TYPE.provider = 'openstack'
CLOUD_SERVICE_TYPE.name = 'Volume'
CLOUD_SERVICE_TYPE.group = 'Storage'
CLOUD_SERVICE_TYPE.labels = ['Storage', 'Volume']
CLOUD_SERVICE_TYPE.is_primary = True
CLOUD_SERVICE_TYPE.is_major = True
CLOUD_SERVICE_TYPE.service_code = 'OSBlockStorage'
CLOUD_SERVICE_TYPE.tags = {
    'spaceone:icon': 'https://wiki.openstack.org/wiki/File:Swift-complete-300.svg',
    'spaceone:display_name': 'BlockStorage'
}

CST_VOLUME_META = CSTMetaGenerator()
CST_VOLUME_META.set_cst_meta_field(TextDyField, 'Name', 'data.name')
CST_VOLUME_META.set_cst_meta_field(TextDyField, 'ID', 'data.id')
CST_VOLUME_META.set_cst_meta_field(EnumDyField, 'Status', 'data.status', default_state={
    'safe': ['ACTIVE'],
    'available': ['BUILD', 'PAUSED'],
    'warning': ['MIGRATING', 'HARD_REBOOT', 'PASSWORD', 'REBOOT', 'REBUILD', 'RESCUE', 'SHUTOFF', 'SUSPENDED'],
    'disable': ['DELETED'],
    'alert': ['ERROR']
})
CST_VOLUME_META.set_cst_meta_field(TextDyField, 'Size(GB)', 'data.size_gb')
CST_VOLUME_META.set_cst_meta_field(TextDyField, 'Image Name', 'data.volume_image_metadata.image_name')
CST_VOLUME_META.set_cst_meta_field(TextDyField, 'Type', 'data.volume_type')
CST_VOLUME_META.set_cst_meta_field(EnumDyField, 'Multi attach', 'data.multiattach', default_badge={
    'indigo.500': ['true'], 'coral.600': ['false']
})
CST_VOLUME_META.set_cst_meta_field(TextDyField, 'Attached VM', 'data.attachments.server_id',
                                   reference={"resource_type": "inventory.CloudService",
                                              "reference_key": "reference.resource_id"})
CST_VOLUME_META.set_cst_meta_field(TextDyField, 'Device', 'data.attachments.device')
CST_VOLUME_META.set_cst_meta_field(TextDyField, 'Availability Zone', 'data.availability_zone')
CST_VOLUME_META.set_cst_meta_field(EnumDyField, 'Bootable', 'data.is_bootable', default_badge={
    'indigo.500': ['true'], 'coral.600': ['false']})
CST_VOLUME_META.set_cst_meta_field(TextDyField, 'Source Volume ID', 'data.source_volume_id',
                                   options={'is_optional': True})
CST_VOLUME_META.set_cst_meta_field(TextDyField, 'Host Name', 'data.attachments.host_name',
                                   options={'is_optional': True})
CST_VOLUME_META.set_cst_meta_field(TextDyField, 'Encrypted', 'data.is_encrypted', options={'is_optional': True}),
CST_VOLUME_META.set_cst_meta_field(DateTimeDyField, 'Created', 'data.created_at')

CLOUD_SERVICE_TYPE._metadata = CloudServiceTypeMeta.set_meta(
    fields=CST_VOLUME_META.fields, search=CST_VOLUME_META.search,
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf))
    ]
)
