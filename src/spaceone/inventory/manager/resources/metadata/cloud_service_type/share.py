import os

from spaceone.inventory.libs.common_parser import get_data_from_yaml
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.common.response import CloudServiceTypeResource
from spaceone.inventory.model.view.cloud_service_type import CloudServiceTypeMeta
from spaceone.inventory.model.view.dynamic_field import TextDyField, EnumDyField, DateTimeDyField, BadgeDyField
from spaceone.inventory.model.view.dynamic_widget import ChartWidget, CardWidget

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/share/total_count.yml')
total_share_size_conf = os.path.join(current_dir, 'widget/share/total_share_size.yml')
count_by_project_conf = os.path.join(current_dir, 'widget/share/count_by_project.yml')
count_by_region_conf = os.path.join(current_dir, 'widget/share/count_by_region.yml')
count_by_type_conf = os.path.join(current_dir, 'widget/share/count_by_type.yml')

CLOUD_SERVICE_TYPE = CloudServiceTypeResource()
CLOUD_SERVICE_TYPE.provider = 'openstack'
CLOUD_SERVICE_TYPE.name = 'Share'
CLOUD_SERVICE_TYPE.group = 'Storage'
CLOUD_SERVICE_TYPE.labels = ['Storage', 'Share']
CLOUD_SERVICE_TYPE.is_primary = True
CLOUD_SERVICE_TYPE.is_major = True
CLOUD_SERVICE_TYPE.service_code = 'OSShare'
CLOUD_SERVICE_TYPE.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/openstack/openstack_storage.svg',
    'spaceone:display_name': 'Share'
}

CST_SHARE_META = CSTMetaGenerator()
CST_SHARE_META.append_cst_meta_field(TextDyField, 'Name', 'data.name')
CST_SHARE_META.append_cst_meta_field(TextDyField, 'ID', 'data.id', auto_search=True,
                                     reference={"resource_type": "inventory.CloudService",
                                                "reference_key": "reference.resource_id"},
                                     options={'is_optional': True})
CST_SHARE_META.append_cst_meta_field(EnumDyField, 'Status', 'data.status', default_state={
    'available': ['available'],
    'warning': ['creating', 'manage_starting', 'creating_from_snapshot', 'deleting', 'manage_starting',
                'unmanage_starting',
                'extending', 'shrinking', 'migrating', 'migrating_to', 'replication_change', 'reverting'],
    'disable': ['inactive', 'unmanaged', 'deleted'],
    'alert': ['error', 'error_deleting', 'manage_error', 'unmanage_error', 'extending_error', 'shrinking_error',
              'shrinking_possible_data_loss_error', 'reverting_error']
})
CST_SHARE_META.append_cst_meta_field(TextDyField, 'Size', 'data.size_gb', auto_search=True, data_type=int,
                                     type="size", options={"source_unit": "GB", "display_unit": "GB"})
CST_SHARE_META.append_cst_meta_field(TextDyField, 'Type', 'data.share_type', auto_search=True)
CST_SHARE_META.append_cst_meta_field(EnumDyField, 'Protocol', 'data.share_protocol', auto_search=True,
                                     default_badge={
                                         'coral.600': ['NFS'], 'indigo.500': ['CIFS'], 'peacock.500': ['GLUSTERFS'],
                                         'green.500': ['HDFS'], 'red.500': ['CEPHFS'],
                                         'violet.500': ['MAPRFS']})
CST_SHARE_META.append_cst_meta_field(TextDyField, 'Export', 'data.export_location', auto_search=True)
CST_SHARE_META.append_cst_meta_field(TextDyField, 'Exports', 'data.export_locations', auto_search=True,
                                     options={'is_optional': True})
CST_SHARE_META.append_cst_meta_field(TextDyField, 'Share Network', 'data.share_network_id', auto_search=True,
                                     reference={"resource_type": "inventory.CloudService",
                                                "reference_key": "reference.resource_id"})
CST_SHARE_META.append_cst_meta_field(TextDyField, 'Availability Zone', 'data.availability_zone', auto_search=True)
CST_SHARE_META.append_cst_meta_field(TextDyField, 'Host', 'data.host', auto_search=True)
CST_SHARE_META.append_cst_meta_field(EnumDyField, 'Public', 'data.is_public', auto_search=True,
                                     default_badge={'indigo.500': ['true'], 'coral.600': ['false']})
CST_SHARE_META.append_cst_meta_field(TextDyField, 'Project Name', 'data.project_name', auto_search=True)
CST_SHARE_META.append_cst_meta_field(BadgeDyField, 'Project ID', 'data.project_id', auto_search=True,
                                     reference={"resource_type": "inventory.CloudService",
                                                "reference_key": "reference.resource_id"},
                                     options={'is_optional': True})
CST_SHARE_META.append_cst_meta_field(TextDyField, 'Snapshot', 'data.snapshot_id', auto_search=True,
                                     options={'is_optional': True})
CST_SHARE_META.append_cst_meta_field(TextDyField, 'Source', 'data.source_volume_id', auto_search=True,
                                     options={'is_optional': True})
CST_SHARE_META.append_cst_meta_field(DateTimeDyField, 'Created', 'data.created_at', auto_search=True)

CLOUD_SERVICE_TYPE._metadata = CloudServiceTypeMeta.set_meta(
    fields=CST_SHARE_META.fields, search=CST_SHARE_META.search,
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        CardWidget.set(**get_data_from_yaml(total_share_size_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_type_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_project_conf))
    ]
)
