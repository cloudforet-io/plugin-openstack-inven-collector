import os

from spaceone.inventory.libs.common_parser import get_data_from_yaml
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.common.response import CloudServiceTypeResource
from spaceone.inventory.model.view.cloud_service_type import CloudServiceTypeMeta
from spaceone.inventory.model.view.dynamic_field import TextDyField, EnumDyField, BadgeDyField, DateTimeDyField
from spaceone.inventory.model.view.dynamic_widget import ChartWidget, CardWidget

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/image/total_count.yml')
total_image_size_conf = os.path.join(current_dir, 'widget/image/total_image_size.yml')
count_by_region_conf = os.path.join(current_dir, 'widget/image/count_by_region.yml')

CLOUD_SERVICE_TYPE = CloudServiceTypeResource()
CLOUD_SERVICE_TYPE.provider = 'openstack'
CLOUD_SERVICE_TYPE.name = 'Image'
CLOUD_SERVICE_TYPE.group = 'Compute'
CLOUD_SERVICE_TYPE.labels = ['Image', 'Compute']
CLOUD_SERVICE_TYPE.is_primary = False
CLOUD_SERVICE_TYPE.is_major = False
CLOUD_SERVICE_TYPE.service_code = 'OSImage'
CLOUD_SERVICE_TYPE.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/openstack/openstack_compute.svg',
    'spaceone:display_name': 'Image'
}

CST_IMAGE_META = CSTMetaGenerator()

CST_IMAGE_META.append_cst_meta_field(TextDyField, 'Name', 'data.name')
CST_IMAGE_META.append_cst_meta_field(BadgeDyField, 'ID', 'data.id', auto_search=True,
                                     reference={"resource_type": "inventory.CloudService",
                                                "reference_key": "reference.resource_id"},
                                     options={'is_optional': True})
CST_IMAGE_META.append_cst_meta_field(EnumDyField, 'Status', 'data.status', auto_search=True,
                                     default_state={
                                         'safe': ['ACTIVE'],
                                         'disable': ['DOWN'],
                                         'alert': ['ERROR']})
CST_IMAGE_META.append_cst_meta_field(TextDyField, 'Size', 'data.size_mb', auto_search=True, data_type=int,
                                     type="size", options={"source_unit": "MB"})
CST_IMAGE_META.append_cst_meta_field(TextDyField, 'Disk Format', 'data.disk_format', auto_search=True)
CST_IMAGE_META.append_cst_meta_field(TextDyField, 'Container Format', 'data.container_format', auto_search=True)
CST_IMAGE_META.append_cst_meta_field(EnumDyField, 'Visibility', 'data.visibility', auto_search=True,
                                     default_badge={
                                         'coral.600': ['public'], 'indigo.500': ['community'],
                                         'peacock.500': ['shared'],
                                         'violet.500': ['private']})
CST_IMAGE_META.append_cst_meta_field(EnumDyField, 'Hidden', 'data.is_hidden', auto_search=True,
                                     default_badge={
                                         'indigo.500': ['true'], 'coral.600': ['false']})
CST_IMAGE_META.append_cst_meta_field(EnumDyField, 'Protected', 'data.is_protected', auto_search=True,
                                     default_badge={
                                         'indigo.500': ['true'], 'coral.600': ['false']})
CST_IMAGE_META.append_cst_meta_field(TextDyField, 'Project Name', 'data.project_name', auto_search=True)
CST_IMAGE_META.append_cst_meta_field(BadgeDyField, 'Project ID', 'data.owner_id', auto_search=True,
                                     reference={"resource_type": "inventory.CloudService",
                                                "reference_key": "reference.resource_id"},
                                     )
CST_IMAGE_META.append_cst_meta_field(DateTimeDyField, 'Created', 'data.created_at', auto_search=True)
CST_IMAGE_META.append_cst_meta_field(DateTimeDyField, 'Updated', 'data.updated_at', auto_search=True,
                                     options={'is_optional': True})

CLOUD_SERVICE_TYPE._metadata = CloudServiceTypeMeta.set_meta(
    fields=CST_IMAGE_META.fields, search=CST_IMAGE_META.search,
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        CardWidget.set(**get_data_from_yaml(total_image_size_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_region_conf)),
    ]
)
