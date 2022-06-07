import os

from spaceone.inventory.libs.common_parser import get_data_from_yaml
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.common.response import CloudServiceTypeResource
from spaceone.inventory.model.view.cloud_service_type import CloudServiceTypeMeta
from spaceone.inventory.model.view.dynamic_field import TextDyField, EnumDyField, DateTimeDyField, \
    ListDyField, BadgeDyField
from spaceone.inventory.model.view.dynamic_widget import ChartWidget, CardWidget

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/subnet/total_count.yml')
count_by_region_conf = os.path.join(current_dir, 'widget/subnet/count_by_region.yml')

CLOUD_SERVICE_TYPE = CloudServiceTypeResource()
CLOUD_SERVICE_TYPE.provider = 'openstack'
CLOUD_SERVICE_TYPE.name = 'Subnet'
CLOUD_SERVICE_TYPE.group = 'Network'
CLOUD_SERVICE_TYPE.labels = ['Network', 'Subnet']
CLOUD_SERVICE_TYPE.is_primary = True
CLOUD_SERVICE_TYPE.is_major = True
CLOUD_SERVICE_TYPE.service_code = 'OSSubnet'
CLOUD_SERVICE_TYPE.tags = {
    'spaceone:icon': 'https://wiki.openstack.org/w/images/2/2c/Nova-complete-300.svg',
    'spaceone:display_name': 'Subnet'
}

CST_SUBNET_META = CSTMetaGenerator()

CST_SUBNET_META.append_cst_meta_field(TextDyField, 'Name', 'data.name', auto_search=True)
CST_SUBNET_META.append_cst_meta_field(BadgeDyField, 'ID', 'data.id',  auto_search=True,
                                      reference={"resource_type": "inventory.CloudService",
                                                 "reference_key": "reference.resource_id"})
CST_SUBNET_META.append_cst_meta_field(EnumDyField, 'IP Version', 'data.ip_version', auto_search=True,
                                      default_badge={'coral.600': ['4'], 'indigo.500': ['6']})
CST_SUBNET_META.append_cst_meta_field(EnumDyField, 'DHCP', 'data.is_dhcp_enabled',  auto_search=True,
                                      default_badge={'peacock.600': ['true'], 'indigo.500': ['false']})
CST_SUBNET_META.append_cst_meta_field(TextDyField, 'CIDR', 'data.cidr', auto_search=True)
CST_SUBNET_META.append_cst_meta_field(ListDyField, 'IP Pools', 'data.allocation_pools', auto_search=True)
CST_SUBNET_META.append_cst_meta_field(TextDyField, 'G/W', 'data.gateway_ip', auto_search=True)
CST_SUBNET_META.append_cst_meta_field(ListDyField, 'Routes', 'data.host_routes', auto_search=True)
CST_SUBNET_META.append_cst_meta_field(ListDyField, 'DNS', 'data.dns_nameservers', auto_search=True)
CST_SUBNET_META.append_cst_meta_field(TextDyField, 'Segment ID', 'data.segment_id',  auto_search=True)
CST_SUBNET_META.append_cst_meta_field(DateTimeDyField, 'Created', 'data.created_at', auto_search=True)
CST_SUBNET_META.append_cst_meta_field(DateTimeDyField, 'Updated', 'data.updated_at', auto_search=True)

CLOUD_SERVICE_TYPE._metadata = CloudServiceTypeMeta.set_meta(fields=CST_SUBNET_META.fields,
                                                             search=CST_SUBNET_META.search,
                                                             widget=[
                                                                 CardWidget.set(**get_data_from_yaml(total_count_conf)),
                                                                 ChartWidget.set(
                                                                     **get_data_from_yaml(count_by_region_conf)),
                                                             ]
                                                             )
