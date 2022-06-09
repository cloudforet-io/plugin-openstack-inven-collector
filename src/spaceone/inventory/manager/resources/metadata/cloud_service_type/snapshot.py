import os

from spaceone.inventory.libs.common_parser import get_data_from_yaml
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.common.response import CloudServiceTypeResource
from spaceone.inventory.model.view.cloud_service_type import CloudServiceTypeMeta
from spaceone.inventory.model.view.dynamic_field import TextDyField, EnumDyField, BadgeDyField, DateTimeDyField
from spaceone.inventory.model.view.dynamic_widget import ChartWidget, CardWidget

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/snapshot/total_count.yml')
count_by_region_conf = os.path.join(current_dir, 'widget/snapshot/count_by_region.yml')

CLOUD_SERVICE_TYPE = CloudServiceTypeResource()
CLOUD_SERVICE_TYPE.provider = 'openstack'
CLOUD_SERVICE_TYPE.name = 'Snapshot'
CLOUD_SERVICE_TYPE.group = 'Storage'
CLOUD_SERVICE_TYPE.labels = ['Snapshot', 'Storage']
CLOUD_SERVICE_TYPE.is_primary = False
CLOUD_SERVICE_TYPE.is_major = False
CLOUD_SERVICE_TYPE.service_code = 'OSSnapshot'
CLOUD_SERVICE_TYPE.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/openstack/openstack_storage.svg',
    'spaceone:display_name': 'Snapshot'
}

CST_SNAPSHOT_META = CSTMetaGenerator()

CST_SNAPSHOT_META.append_cst_meta_field(TextDyField, 'Name', 'data.name')
CST_SNAPSHOT_META.append_cst_meta_field(TextDyField, 'ID', 'data.id', auto_search=True,
                                        options={'is_optional': True})
CST_SNAPSHOT_META.append_cst_meta_field(EnumDyField, 'Status', 'data.status', auto_search=True,
                                        default_state={
                                            'safe': ['in-use'],
                                            'available': ['available', 'reserved'],
                                            'warning': ['creating', 'backing-up', 'deleting', 'unmanaging', 'restoring'],
                                            'disable': ['deleted'],
                                            'alert': ['error', 'error_deleting']
                                        })
CST_SNAPSHOT_META.append_cst_meta_field(TextDyField, 'Size', 'data.size_gb', auto_search=True, data_type=int,
                                        type="size", options={"source_unit": "GB"})
CST_SNAPSHOT_META.append_cst_meta_field(BadgeDyField, 'Volume ID', 'data.volume_id', auto_search=True,
                                        reference={"resource_type": "inventory.CloudService",
                                                   "reference_key": "reference.resource_id"},
                                        )
CST_SNAPSHOT_META.append_cst_meta_field(TextDyField, 'Project Name', 'data.project_name', auto_search=True)
CST_SNAPSHOT_META.append_cst_meta_field(BadgeDyField, 'Project ID', 'data.project_id', auto_search=True,
                                        reference={"resource_type": "inventory.CloudService",
                                                   "reference_key": "reference.resource_id"},
                                        )
CST_SNAPSHOT_META.append_cst_meta_field(DateTimeDyField, 'Created', 'data.created_at', auto_search=True)

CLOUD_SERVICE_TYPE._metadata = CloudServiceTypeMeta.set_meta(
    fields=CST_SNAPSHOT_META.fields, search=CST_SNAPSHOT_META.search,
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_region_conf)),
    ]
)
