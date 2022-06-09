import os

from spaceone.inventory.libs.common_parser import get_data_from_yaml
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.common.response import CloudServiceTypeResource
from spaceone.inventory.model.view.cloud_service_type import CloudServiceTypeMeta
from spaceone.inventory.model.view.dynamic_field import TextDyField, EnumDyField, BadgeDyField, DateTimeDyField, \
    ListDyField
from spaceone.inventory.model.view.dynamic_widget import ChartWidget, CardWidget

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/router/total_count.yml')
count_by_region_conf = os.path.join(current_dir, 'widget/router/count_by_region.yml')

CLOUD_SERVICE_TYPE = CloudServiceTypeResource()
CLOUD_SERVICE_TYPE.provider = 'openstack'
CLOUD_SERVICE_TYPE.name = 'Router'
CLOUD_SERVICE_TYPE.group = 'Network'
CLOUD_SERVICE_TYPE.labels = ['Network', 'Router']
CLOUD_SERVICE_TYPE.is_primary = False
CLOUD_SERVICE_TYPE.is_major = False
CLOUD_SERVICE_TYPE.service_code = 'OSRouter'
CLOUD_SERVICE_TYPE.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/openstack/openstack_network.svg',
    'spaceone:display_name': 'Router'
}

CST_ROUTER_META = CSTMetaGenerator()

CST_ROUTER_META.append_cst_meta_field(TextDyField, 'Name', 'data.name', auto_search=True)
CST_ROUTER_META.append_cst_meta_field(TextDyField, 'ID', 'data.id', auto_search=True,
                                      options={'is_optional': True})
CST_ROUTER_META.append_cst_meta_field(EnumDyField, 'Status', 'data.status', auto_search=True,
                                      default_state={
                                          'safe': ['ACTIVE'],
                                          'disable': ['DOWN'],
                                          'alert': ['ERROR']})
CST_ROUTER_META.append_cst_meta_field(BadgeDyField, 'External G/W Network ID', 'data.external_gateway_info.network_id',
                                      auto_search=True,
                                      reference={"resource_type": "inventory.CloudService",
                                                 "reference_key": "reference.resource_id"},
                                      )
CST_ROUTER_META.append_cst_meta_field(EnumDyField, 'Admin Status', 'data.is_admin_state_up', auto_search=True,
                                      default_badge={
                                          'green.500': ['true'], 'red.600': ['false']
                                      })
CST_ROUTER_META.append_cst_meta_field(ListDyField, 'Availability Zones', 'data.availability_zones', auto_search=True)
CST_ROUTER_META.append_cst_meta_field(TextDyField, 'Project Name', 'data.project_name', auto_search=True)
CST_ROUTER_META.append_cst_meta_field(BadgeDyField, 'Project ID', 'data.project_id', auto_search=True,
                                      reference={"resource_type": "inventory.CloudService",
                                                 "reference_key": "reference.resource_id"},
                                      )
CST_ROUTER_META.append_cst_meta_field(DateTimeDyField, 'Created', 'data.created_at', auto_search=True)
CST_ROUTER_META.append_cst_meta_field(DateTimeDyField, 'Updated', 'data.updated_at', auto_search=True,
                                      options={'is_optional': True})

CLOUD_SERVICE_TYPE._metadata = CloudServiceTypeMeta.set_meta(
    fields=CST_ROUTER_META.fields, search=CST_ROUTER_META.search,
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_region_conf)),
    ]
)
