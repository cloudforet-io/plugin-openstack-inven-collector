import os
from spaceone.inventory.libs import common_parser
from spaceone.inventory.model.view.dynamic_widget import ChartWidget, CardWidget
from spaceone.inventory.model.view.dynamic_field import TextDyField, EnumDyField, SearchField, DateTimeDyField, \
    SizeField, ListDyField
from spaceone.inventory.model.common.response import CloudServiceTypeResource, CloudServiceTypeResponse
from spaceone.inventory.model.view.cloud_service_type import CloudServiceTypeMeta
from spaceone.inventory.libs.metaman import CSTMetaGenerator

current_dir = os.path.abspath(os.path.dirname(__file__))

CLOUD_SERVICE_TYPE = CloudServiceTypeResource()
CLOUD_SERVICE_TYPE.provider = 'openstack'
CLOUD_SERVICE_TYPE.name = 'Network'
CLOUD_SERVICE_TYPE.group = 'Network'
CLOUD_SERVICE_TYPE.labels = ['Compute', 'Network']
CLOUD_SERVICE_TYPE.is_primary = True
CLOUD_SERVICE_TYPE.is_major = True
CLOUD_SERVICE_TYPE.service_code = 'OSNetwork'
CLOUD_SERVICE_TYPE.tags = {
    'spaceone:icon': 'https://wiki.openstack.org/w/images/2/2c/Nova-complete-300.svg',
    'spaceone:display_name': 'Network'
}

CST_NETWORK_META = CSTMetaGenerator()

CST_NETWORK_META.set_cst_meta_field(TextDyField, 'Name', 'data.name')
CST_NETWORK_META.set_cst_meta_field(TextDyField, 'ID', 'data.id')
CST_NETWORK_META.set_cst_meta_field(EnumDyField, 'Status', 'data.status', default_state={
            'safe': ['ACTIVE'],
            'available': ['BUILD', 'PAUSED'],
            'warning': ['MIGRATING', 'HARD_REBOOT', 'PASSWORD', 'REBOOT', 'REBUILD', 'RESCUE', 'SHUTOFF', 'SUSPENDED'],
            'disable': ['DELETED'],
            'alert': ['ERROR']
        })
CST_NETWORK_META.set_cst_meta_field(ListDyField, 'Subnet', 'data.minimal_subnets')
CST_NETWORK_META.set_cst_meta_field(ListDyField, 'Subnet ids', 'data.subnets.id', options={'is_optional': True})
CST_NETWORK_META.set_cst_meta_field(TextDyField, 'MTU', 'data.mtu')
CST_NETWORK_META.set_cst_meta_field(EnumDyField, 'Shared', 'data.is_shared', default_badge={
            'indigo.500': ['true'], 'coral.600': ['false']
        })
CST_NETWORK_META.set_cst_meta_field(EnumDyField, 'Port Security', 'data.is_port_security_enabled', default_badge={
            'indigo.500': ['true'], 'coral.600': ['false']
        })
CST_NETWORK_META.set_cst_meta_field(EnumDyField, 'Vlan Transparent', 'data.vlan_transparent', default_badge={
            'indigo.500': ['true'], 'coral.600': ['false']
        })
CST_NETWORK_META.set_cst_meta_field(EnumDyField, 'Admin Status', 'data.is_admin_state_up', efault_badge={
            'indigo.500': ['true'], 'coral.600': ['false']
        })
CST_NETWORK_META.set_cst_meta_field(ListDyField, 'Segments', 'data.segments.id', options={'is_optional': True})
CST_NETWORK_META.set_cst_meta_field(ListDyField, 'Availability Zone', 'data.availability_zones')
CST_NETWORK_META.set_cst_meta_field(DateTimeDyField, 'Created', 'data.created_at')
CST_NETWORK_META.set_cst_meta_field(DateTimeDyField, 'Updated', 'data.created_at', options={'is_optional': True})

CLOUD_SERVICE_TYPE._metadata = CloudServiceTypeMeta.set_meta(
    fields=CST_NETWORK_META.fields, search=CST_NETWORK_META.search
)

