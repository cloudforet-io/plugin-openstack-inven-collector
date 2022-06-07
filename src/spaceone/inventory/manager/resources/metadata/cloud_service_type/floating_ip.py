import os

from spaceone.inventory.libs.common_parser import get_data_from_yaml
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.common.response import CloudServiceTypeResource
from spaceone.inventory.model.view.cloud_service_type import CloudServiceTypeMeta
from spaceone.inventory.model.view.dynamic_field import TextDyField, EnumDyField, BadgeDyField, DateTimeDyField
from spaceone.inventory.model.view.dynamic_widget import ChartWidget, CardWidget

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/floating_ip/total_count.yml')
count_by_region_conf = os.path.join(current_dir, 'widget/floating_ip/count_by_region.yml')

CLOUD_SERVICE_TYPE = CloudServiceTypeResource()
CLOUD_SERVICE_TYPE.provider = 'openstack'
CLOUD_SERVICE_TYPE.name = 'Floating IP'
CLOUD_SERVICE_TYPE.group = 'Network'
CLOUD_SERVICE_TYPE.labels = ['Network', 'Floating IP']
CLOUD_SERVICE_TYPE.is_primary = False
CLOUD_SERVICE_TYPE.is_major = False
CLOUD_SERVICE_TYPE.service_code = 'OSFloatingIP'
CLOUD_SERVICE_TYPE.tags = {
    'spaceone:icon': 'https://wiki.openstack.org/w/images/2/2c/Nova-complete-300.svg',
    'spaceone:display_name': 'FloatingIP'
}

CST_FLOATING_IP_META = CSTMetaGenerator()

CST_FLOATING_IP_META.append_cst_meta_field(TextDyField, 'Name', 'data.name', auto_search=True)
CST_FLOATING_IP_META.append_cst_meta_field(TextDyField, 'ID', 'data.id', auto_search=True,
                                           options={'is_optional': True})
CST_FLOATING_IP_META.append_cst_meta_field(EnumDyField, 'Status', 'data.status', auto_search=True,
                                           default_state={
                                               'safe': ['ACTIVE'],
                                               'disable': ['DOWN'],
                                               'alert': ['ERROR']})
CST_FLOATING_IP_META.append_cst_meta_field(TextDyField, 'DNS Domain', 'data.dns_domain', auto_search=True)
CST_FLOATING_IP_META.append_cst_meta_field(TextDyField, 'DNS Name', 'data.dns_name', auto_search=True)
CST_FLOATING_IP_META.append_cst_meta_field(TextDyField, 'Floating Ip Address', 'data.floating_ip_address',
                                           auto_search=True)
CST_FLOATING_IP_META.append_cst_meta_field(TextDyField, 'Fixed Ip Address', 'data.fixed_ip_address', auto_search=True)
CST_FLOATING_IP_META.append_cst_meta_field(BadgeDyField, 'Device ID', 'data.port_details.device_id', auto_search=True,
                                           reference={"resource_type": "inventory.CloudService",
                                                      "reference_key": "reference.resource_id"},
                                           )
CST_FLOATING_IP_META.append_cst_meta_field(TextDyField, 'Project Name', 'data.project_name', auto_search=True)
CST_FLOATING_IP_META.append_cst_meta_field(BadgeDyField, 'Project ID', 'data.project_id', auto_search=True,
                                           reference={"resource_type": "inventory.CloudService",
                                                      "reference_key": "reference.resource_id"},
                                           )
CST_FLOATING_IP_META.append_cst_meta_field(TextDyField, 'QoS Policy ID', 'data.qos_policy_id', auto_search=True)
CST_FLOATING_IP_META.append_cst_meta_field(BadgeDyField, 'Route ID', 'data.router_id', auto_search=True,
                                           reference={"resource_type": "inventory.CloudService",
                                                      "reference_key": "reference.resource_id"},
                                           )
CST_FLOATING_IP_META.append_cst_meta_field(BadgeDyField, 'Network ID', 'data.floating_network_id', auto_search=True,
                                           reference={"resource_type": "inventory.CloudService",
                                                      "reference_key": "reference.resource_id"},
                                           )
CST_FLOATING_IP_META.append_cst_meta_field(DateTimeDyField, 'Created', 'data.created_at', auto_search=True)
CST_FLOATING_IP_META.append_cst_meta_field(DateTimeDyField, 'Updated', 'data.updated_at', auto_search=True,
                                           options={'is_optional': True})

CLOUD_SERVICE_TYPE._metadata = CloudServiceTypeMeta.set_meta(
    fields=CST_FLOATING_IP_META.fields, search=CST_FLOATING_IP_META.search,
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_region_conf)),
    ]
)
