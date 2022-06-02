from spaceone.inventory.manager.resources.metadata.cloud_service_type.network import CST_NETWORK_META
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.view.cloud_service import CloudServiceMeta
from spaceone.inventory.model.view.dynamic_field import TextDyField, ListDyField, DateTimeDyField, \
    EnumDyField, BadgeDyField
from spaceone.inventory.model.view.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, SimpleTableDynamicLayout

CST_NETWORK_META.insert_cst_meta_field('ID', TextDyField, 'Description', 'data.description')
CST_NETWORK_META.append_cst_meta_field(TextDyField, 'externalLink', 'data.external_link')

CLOUD_SERVICE_BASE = ItemDynamicLayout.set_fields('Network', fields=CST_NETWORK_META.fields)

CS_NETWORK_SUBNET_META = CSTMetaGenerator()

CS_NETWORK_SUBNET_META.append_cst_meta_field(TextDyField, 'Name', 'name')
CS_NETWORK_SUBNET_META.append_cst_meta_field(BadgeDyField, 'ID', 'id',
                                             reference={"resource_type": "inventory.CloudService",
                                                        "reference_key": "reference.resource_id"}, )
CS_NETWORK_SUBNET_META.append_cst_meta_field(TextDyField, 'Description', 'description')
CS_NETWORK_SUBNET_META.append_cst_meta_field(EnumDyField, 'IP Version', 'ip_version',
                                             default_badge={'coral.600': ['4'], 'indigo.500': ['6']})
CS_NETWORK_SUBNET_META.append_cst_meta_field(EnumDyField, 'DHCP', 'is_dhcp_enabled',
                                             default_badge={'peacock.600': ['true'], 'indigo.500': ['false']})
CS_NETWORK_SUBNET_META.append_cst_meta_field(TextDyField, 'CIDR', 'cidr')
CS_NETWORK_SUBNET_META.append_cst_meta_field(ListDyField, 'IP Pools', 'allocation_pools')
CS_NETWORK_SUBNET_META.append_cst_meta_field(TextDyField, 'G/W', 'gateway_ip')
CS_NETWORK_SUBNET_META.append_cst_meta_field(ListDyField, 'Routes', 'host_routes')
CS_NETWORK_SUBNET_META.append_cst_meta_field(ListDyField, 'DNS', 'dns_nameservers')
CS_NETWORK_SUBNET_META.append_cst_meta_field(TextDyField, 'Segment ID', 'segment_id')
CS_NETWORK_SUBNET_META.append_cst_meta_field(DateTimeDyField, 'Created', 'created_at')
CS_NETWORK_SUBNET_META.append_cst_meta_field(DateTimeDyField, 'Updated', 'updated_at')

CLOUD_SERVICE_SUBNET = TableDynamicLayout.set_fields('Subnets', root_path="data.subnets",
                                                     fields=CS_NETWORK_SUBNET_META.fields)

CS_NETWORK_SEGMENT_META = CSTMetaGenerator()

CS_NETWORK_SEGMENT_META.append_cst_meta_field(TextDyField, 'Segmentation ID', 'provider:segmentation_id')
CS_NETWORK_SEGMENT_META.append_cst_meta_field(TextDyField, 'Physical Network', 'provider:physical_network')
CS_NETWORK_SEGMENT_META.append_cst_meta_field(TextDyField, 'Network Type', 'provider:network_type')

CLOUD_SERVICE_SEGMENT = SimpleTableDynamicLayout.set_fields('Segments', root_path="data.segments",
                                                            fields=CS_NETWORK_SEGMENT_META.fields)

CLOUD_SERVICE_METADATA = CloudServiceMeta.set_layouts(
    layouts=[CLOUD_SERVICE_BASE, CLOUD_SERVICE_SUBNET, CLOUD_SERVICE_SEGMENT])
