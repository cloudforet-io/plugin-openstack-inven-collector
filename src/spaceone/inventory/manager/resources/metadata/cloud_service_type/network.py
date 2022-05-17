import os

from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.common.response import CloudServiceTypeResource
from spaceone.inventory.model.view.cloud_service_type import CloudServiceTypeMeta
from spaceone.inventory.model.view.dynamic_field import TextDyField, EnumDyField, DateTimeDyField, \
    ListDyField

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

CST_NETWORK_META.append_cst_meta_field(TextDyField, 'Name', 'data.name')
CST_NETWORK_META.append_cst_meta_field(TextDyField, 'ID', 'data.id', auto_search=True,
                                       reference={"resource_type": "inventory.CloudService",
                                                  "reference_key": "reference.resource_id"},
                                       options={'is_optional': True})
CST_NETWORK_META.append_cst_meta_field(EnumDyField, 'Status', 'data.status', auto_search=True,
                                       default_state={
                                           'safe': ['ACTIVE'],
                                           'available': ['BUILD', 'PAUSED'],
                                           'warning': ['MIGRATING', 'HARD_REBOOT', 'PASSWORD', 'REBOOT', 'REBUILD',
                                                       'RESCUE', 'SHUTOFF', 'SUSPENDED'],
                                           'disable': ['DELETED'],
                                           'alert': ['ERROR']
                                       })
CST_NETWORK_META.append_cst_meta_field(ListDyField, 'CIDRs', 'data.cidrs', auto_search=True,
                                       options={'is_optional': True})
CST_NETWORK_META.append_cst_meta_field(ListDyField, 'Subnet', 'data.minimal_subnets', auto_search=True)
CST_NETWORK_META.append_cst_meta_field(ListDyField, 'Subnet ids', 'data.subnets.id', auto_search=True,
                                       options={'is_optional': True})
CST_NETWORK_META.append_cst_meta_field(TextDyField, 'MTU', 'data.mtu', auto_search=True)
CST_NETWORK_META.append_cst_meta_field(EnumDyField, 'Shared', 'data.is_shared', auto_search=True,
                                       default_badge={
                                           'indigo.500': ['true'], 'coral.600': ['false']
                                       })
CST_NETWORK_META.append_cst_meta_field(EnumDyField, 'Port Security', 'data.is_port_security_enabled', auto_search=True,
                                       default_badge={
                                           'indigo.500': ['true'], 'coral.600': ['false']
                                       })
CST_NETWORK_META.append_cst_meta_field(EnumDyField, 'Vlan Transparent', 'data.vlan_transparent', auto_search=True,
                                       default_badge={
                                           'indigo.500': ['true'], 'coral.600': ['false']
                                       })
CST_NETWORK_META.append_cst_meta_field(EnumDyField, 'Admin Status', 'data.is_admin_state_up', auto_search=True,
                                       default_badge={
                                           'green.500': ['true'], 'red.600': ['false']
                                       })
CST_NETWORK_META.append_cst_meta_field(ListDyField, 'Segments', 'data.segments.id', auto_search=True,
                                       options={'is_optional': True})
CST_NETWORK_META.append_cst_meta_field(ListDyField, 'Availability Zone', 'data.availability_zones', auto_search=True)
CST_NETWORK_META.append_cst_meta_field(TextDyField, 'Project Name', 'data.project_name', auto_search=True)
CST_NETWORK_META.append_cst_meta_field(TextDyField, 'Project ID', 'data.project_id', auto_search=True,
                                       options={'is_optional': True})
CST_NETWORK_META.append_cst_meta_field(DateTimeDyField, 'Created', 'data.created_at', auto_search=True)
CST_NETWORK_META.append_cst_meta_field(DateTimeDyField, 'Updated', 'data.created_at', auto_search=True,
                                       options={'is_optional': True})

CLOUD_SERVICE_TYPE._metadata = CloudServiceTypeMeta.set_meta(
    fields=CST_NETWORK_META.fields, search=CST_NETWORK_META.search
)
