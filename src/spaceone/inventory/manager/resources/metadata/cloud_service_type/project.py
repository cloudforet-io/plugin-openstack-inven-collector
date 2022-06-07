import os

from spaceone.inventory.libs.common_parser import get_data_from_yaml
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.common.response import CloudServiceTypeResource
from spaceone.inventory.model.view.cloud_service_type import CloudServiceTypeMeta
from spaceone.inventory.model.view.dynamic_field import TextDyField, EnumDyField, BadgeDyField
from spaceone.inventory.model.view.dynamic_widget import ChartWidget, CardWidget

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/project/total_count.yml')
count_by_region_conf = os.path.join(current_dir, 'widget/project/count_by_region.yml')

CLOUD_SERVICE_TYPE = CloudServiceTypeResource()
CLOUD_SERVICE_TYPE.provider = 'openstack'
CLOUD_SERVICE_TYPE.name = 'Project'
CLOUD_SERVICE_TYPE.group = 'Identity'
CLOUD_SERVICE_TYPE.labels = ['Identity', 'Project']
CLOUD_SERVICE_TYPE.is_primary = True
CLOUD_SERVICE_TYPE.is_major = True
CLOUD_SERVICE_TYPE.service_code = 'OSProject'
CLOUD_SERVICE_TYPE.tags = {
    'spaceone:icon': 'https://wiki.openstack.org/wiki/File:Swift-complete-300.svg',
    'spaceone:display_name': 'Project'
}

CST_PROJECT_META = CSTMetaGenerator()
CST_PROJECT_META.append_cst_meta_field(TextDyField, 'Name', 'data.name')
CST_PROJECT_META.append_cst_meta_field(BadgeDyField, 'ID', 'data.id', auto_search=True,
                                       reference={"resource_type": "inventory.CloudService",
                                                  "reference_key": "reference.resource_id"},
                                       options={'is_optional': True})
CST_PROJECT_META.append_cst_meta_field(TextDyField, 'Domain ID', 'data.domain_id', auto_search=True)
CST_PROJECT_META.append_cst_meta_field(EnumDyField, 'Is Domain', 'data.is_domain', auto_search=True,
                                       default_badge={'indigo.500': ['true'], 'coral.600': ['false']})
CST_PROJECT_META.append_cst_meta_field(EnumDyField, 'Enabled', 'data.is_enabled', auto_search=True,
                                       default_badge={'indigo.500': ['true'], 'coral.600': ['false']})
CST_PROJECT_META.append_cst_meta_field(TextDyField, 'Parent ID', 'data.parent_id', auto_search=True)

CLOUD_SERVICE_TYPE._metadata = CloudServiceTypeMeta.set_meta(
    fields=CST_PROJECT_META.fields, search=CST_PROJECT_META.search,
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_region_conf)),
    ]
)
