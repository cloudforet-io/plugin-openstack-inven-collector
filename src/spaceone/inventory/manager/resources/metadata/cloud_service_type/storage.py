import os

from spaceone.inventory.libs.common_parser import get_data_from_yaml
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.common.response import CloudServiceTypeResource
from spaceone.inventory.model.view.cloud_service_type import CloudServiceTypeMeta
from spaceone.inventory.model.view.dynamic_field import TextDyField, EnumDyField, BadgeDyField
from spaceone.inventory.model.view.dynamic_widget import ChartWidget, CardWidget

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/storage/total_count.yml')
total_volume_count_conf = os.path.join(current_dir, 'widget/storage/total_volume_count.yml')
total_allocated_volume_size_conf = os.path.join(current_dir, 'widget/storage/total_allocated_volume_size.yml')
volume_size_by_backend_name_conf = os.path.join(current_dir, 'widget/storage/volume_size_by_backend_name.yml')
count_by_region_conf = os.path.join(current_dir, 'widget/storage/count_by_region.yml')
count_by_backend_name_conf = os.path.join(current_dir, 'widget/storage/count_by_backend_name.yml')

CLOUD_SERVICE_TYPE = CloudServiceTypeResource()
CLOUD_SERVICE_TYPE.provider = 'openstack'
CLOUD_SERVICE_TYPE.name = 'Storage'
CLOUD_SERVICE_TYPE.group = 'Storage'
CLOUD_SERVICE_TYPE.labels = ['Storage', 'Storage']
CLOUD_SERVICE_TYPE.is_primary = False
CLOUD_SERVICE_TYPE.is_major = False
CLOUD_SERVICE_TYPE.service_code = 'OSStorage'
CLOUD_SERVICE_TYPE.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/openstack/openstack_storage.svg',
    'spaceone:display_name': 'Storage'
}

CST_STORAGE_META = CSTMetaGenerator()

CST_STORAGE_META.append_cst_meta_field(TextDyField, 'Name', 'data.name')
CST_STORAGE_META.append_cst_meta_field(BadgeDyField, 'ID', 'data.id', auto_search=True,
                                       reference={"resource_type": "inventory.CloudService",
                                                  "reference_key": "reference.resource_id"},
                                       options={'is_optional': True})
CST_STORAGE_META.append_cst_meta_field(TextDyField, 'Display Name', 'data.display_name', auto_search=True,
                                       options={'is_optional': True})
CST_STORAGE_META.append_cst_meta_field(TextDyField, 'Namespace', 'data.namespace', auto_search=True,
                                       options={'is_optional': True})
CST_STORAGE_META.append_cst_meta_field(EnumDyField, 'Protocol', 'data.storage_protocol', auto_search=True,
                                       default_badge={
                                           'coral.600': ['nfs'], 'indigo.500': ['iSCSI'], 'peacock.500': ['cephfs']})
CST_STORAGE_META.append_cst_meta_field(EnumDyField, 'Vendor', 'data.vendor_name', auto_search=True,
                                       default_badge={
                                           'blue.600': ['NetApp'], 'indigo.500': ['HPE'], 'peacock.500': ['EMC'],
                                           'green.500': ['Open Source'], 'red.500': ['Dell'], 'violet.500': ['Ceph']})
CST_STORAGE_META.append_cst_meta_field(TextDyField, 'Backend Name', 'data.volume_backend_name', auto_search=True)

CST_STORAGE_META.append_cst_meta_field(TextDyField, 'Allocated Volume Size', 'data.total_allocated_volume_size',
                                       auto_search=True, data_type=int, type="size",
                                       options={"source_unit": "GB", "display_unit": "GB"})
CST_STORAGE_META.append_cst_meta_field(TextDyField, 'Volume Count', 'data.total_volume_count',
                                       auto_search=True, data_type=int)
CST_STORAGE_META.append_cst_meta_field(TextDyField, 'Attached Volume Count', 'data.attached_volume_count',
                                       auto_search=True, data_type=int)
CST_STORAGE_META.append_cst_meta_field(TextDyField, 'Available Volume Count', 'data.available_volume_count',
                                       auto_search=True, data_type=int)

CST_STORAGE_META.append_cst_meta_field(TextDyField, 'Driver Version', 'data.driver_version', auto_search=True)

CLOUD_SERVICE_TYPE._metadata = CloudServiceTypeMeta.set_meta(
    fields=CST_STORAGE_META.fields, search=CST_STORAGE_META.search,
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        CardWidget.set(**get_data_from_yaml(total_volume_count_conf)),
        CardWidget.set(**get_data_from_yaml(total_allocated_volume_size_conf)),
        ChartWidget.set(
            **get_data_from_yaml(count_by_region_conf)),
        ChartWidget.set(
            **get_data_from_yaml(count_by_backend_name_conf)),
        ChartWidget.set(
            **get_data_from_yaml(volume_size_by_backend_name_conf))
    ]
)
