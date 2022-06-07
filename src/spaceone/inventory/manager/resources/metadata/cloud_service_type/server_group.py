import os

from spaceone.inventory.libs.common_parser import get_data_from_yaml
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.common.response import CloudServiceTypeResource
from spaceone.inventory.model.view.cloud_service_type import CloudServiceTypeMeta
from spaceone.inventory.model.view.dynamic_field import TextDyField, EnumDyField, BadgeDyField, ListDyField
from spaceone.inventory.model.view.dynamic_widget import ChartWidget, CardWidget

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/server_group/total_count.yml')
count_by_region_conf = os.path.join(current_dir, 'widget/server_group/count_by_region.yml')

CLOUD_SERVICE_TYPE = CloudServiceTypeResource()
CLOUD_SERVICE_TYPE.provider = 'openstack'
CLOUD_SERVICE_TYPE.name = 'Server Group'
CLOUD_SERVICE_TYPE.group = 'Compute'
CLOUD_SERVICE_TYPE.labels = ['Compute', 'Server Group']
CLOUD_SERVICE_TYPE.is_primary = False
CLOUD_SERVICE_TYPE.is_major = False
CLOUD_SERVICE_TYPE.service_code = 'OSServerGroup'
CLOUD_SERVICE_TYPE.tags = {
    'spaceone:icon': 'https://wiki.openstack.org/w/images/2/2c/Nova-complete-300.svg',
    'spaceone:display_name': 'ServerGroup'
}

CST_SG_META = CSTMetaGenerator()

CST_SG_META.append_cst_meta_field(TextDyField, 'Name', 'data.name')
CST_SG_META.append_cst_meta_field(BadgeDyField, 'ID', 'data.id', auto_search=True,
                                  reference={"resource_type": "inventory.CloudService",
                                             "reference_key": "reference.resource_id"},
                                  options={'is_optional': True})
CST_SG_META.append_cst_meta_field(EnumDyField, 'Policy', 'data.policy', auto_search=True,
                                  default_badge={
                                      'coral.600': ['anti-affinity'], 'indigo.500': ['affinity'],
                                      'peacock.500': ['soft-anti-affinity'], 'violet.500': ['soft-affinity']})
CST_SG_META.append_cst_meta_field(TextDyField, 'Instance Count', 'data.member_count', auto_search=True, data_type=int)
CST_SG_META.append_cst_meta_field(ListDyField, 'Instances', 'data.member_ids', auto_search=True,
                                  reference={"resource_type": "inventory.CloudService",
                                             "reference_key": "reference.resource_id"},
                                  default_badge={"type": "reference", 'delimiter': ' ', 'sub_key': 'server_id'},
                                  options={'is_optional': True}
                                  )
CST_SG_META.append_cst_meta_field(TextDyField, 'Project Name', 'data.project_name', auto_search=True)
CST_SG_META.append_cst_meta_field(BadgeDyField, 'Project Id', 'data.project_id', auto_search=True,
                                  reference={"resource_type": "inventory.CloudService",
                                             "reference_key": "reference.resource_id"},
                                  )
CST_SG_META.append_cst_meta_field(BadgeDyField, 'User Id', 'data.user_id', auto_search=True,
                                  reference={"resource_type": "inventory.CloudService",
                                             "reference_key": "reference.resource_id"},
                                  )

CLOUD_SERVICE_TYPE._metadata = CloudServiceTypeMeta.set_meta(
    fields=CST_SG_META.fields, search=CST_SG_META.search,
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        ChartWidget.set(
            **get_data_from_yaml(count_by_region_conf))
    ]
)
