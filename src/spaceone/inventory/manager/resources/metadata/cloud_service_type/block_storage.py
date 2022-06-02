import os

from spaceone.inventory.libs.common_parser import get_data_from_yaml
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.common.response import CloudServiceTypeResource
from spaceone.inventory.model.view.cloud_service_type import CloudServiceTypeMeta
from spaceone.inventory.model.view.dynamic_field import TextDyField, EnumDyField, DateTimeDyField, ListDyField, \
    BadgeDyField
from spaceone.inventory.model.view.dynamic_widget import ChartWidget, CardWidget

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/block_storage/total_count.yml')
total_volume_size_conf = os.path.join(current_dir, 'widget/block_storage/total_volume_size.yml')
count_by_project_conf = os.path.join(current_dir, 'widget/block_storage/count_by_project.yml')
count_by_region_conf = os.path.join(current_dir, 'widget/block_storage/count_by_region.yml')
count_by_type_conf = os.path.join(current_dir, 'widget/block_storage/count_by_type.yml')

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
CST_VOLUME_META.append_cst_meta_field(TextDyField, 'Name', 'data.name')
CST_VOLUME_META.append_cst_meta_field(BadgeDyField, 'ID', 'data.id', auto_search=True,
                                      reference={"resource_type": "inventory.CloudService",
                                                 "reference_key": "reference.resource_id"},
                                      options={'is_optional': True})
CST_VOLUME_META.append_cst_meta_field(EnumDyField, 'Status', 'data.status', default_state={
    'safe': ['in-use'],
    'available': ['available', 'reserved'],
    'warning': ['creating', 'attaching', 'maintenance', 'deleting', 'detaching', 'maintenance', 'awaiting-transfer',
                'backing-up', 'downloading', 'uploading', 'retyping', 'extending'],
    'disable': [],
    'alert': ['error', 'error_deleting', 'error_backing-up', 'error_restoring', 'error_extending', '']
})
CST_VOLUME_META.append_cst_meta_field(TextDyField, 'Size', 'data.size_gb', auto_search=True, type="size",
                                      options={"source_unit": "GB"})
CST_VOLUME_META.append_cst_meta_field(TextDyField, 'Image Name', 'data.volume_image_metadata.image_name',
                                      auto_search=True)
CST_VOLUME_META.append_cst_meta_field(TextDyField, 'Type', 'data.volume_type', auto_search=True)
CST_VOLUME_META.append_cst_meta_field(EnumDyField, 'Bootable', 'data.is_bootable', auto_search=True,
                                      default_badge={
                                          'indigo.500': ['true'], 'coral.600': ['false']})
CST_VOLUME_META.append_cst_meta_field(EnumDyField, 'Multi attach', 'data.multiattach', auto_search=True,
                                      default_badge={
                                          'indigo.500': ['true'], 'coral.600': ['false']
                                      })
CST_VOLUME_META.append_cst_meta_field(EnumDyField, 'Encrypted', 'data.is_encrypted',
                                      default_badge={'indigo.500': ['true'], 'coral.600': ['false']})

CST_VOLUME_META.append_cst_meta_field(ListDyField, 'Attached Instances', 'data.attachments', auto_search=True,
                                      reference={"resource_type": "inventory.CloudService",
                                                 "reference_key": "reference.resource_id"},
                                      default_badge={"type": "reference", 'delimiter': ' ', 'sub_key': 'server_id'}
                                      )
CST_VOLUME_META.append_cst_meta_field(ListDyField, 'Device', 'data.attachments.device', auto_search=True)
CST_VOLUME_META.append_cst_meta_field(TextDyField, 'Availability Zone', 'data.availability_zone', auto_search=True)
CST_VOLUME_META.append_cst_meta_field(TextDyField, 'Source Volume ID', 'data.source_volume_id', auto_search=True,
                                      options={'is_optional': True})
CST_VOLUME_META.append_cst_meta_field(BadgeDyField, 'Storage', 'data.host', auto_search=True,
                                      reference={"resource_type": "inventory.CloudService",
                                                 "reference_key": "reference.resource_id"},
                                      options={'is_optional': True})
CST_VOLUME_META.append_cst_meta_field(TextDyField, 'Project Name', 'data.project_name', auto_search=True)
CST_VOLUME_META.append_cst_meta_field(BadgeDyField, 'Project ID', 'data.project_id', auto_search=True,
                                      reference={"resource_type": "inventory.CloudService",
                                                 "reference_key": "reference.resource_id"},
                                      options={'is_optional': True})
CST_VOLUME_META.append_cst_meta_field(DateTimeDyField, 'Created', 'data.created_at', auto_search=True)

CLOUD_SERVICE_TYPE._metadata = CloudServiceTypeMeta.set_meta(
    fields=CST_VOLUME_META.fields, search=CST_VOLUME_META.search,
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        CardWidget.set(**get_data_from_yaml(total_volume_size_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_type_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_project_conf))
    ]
)
