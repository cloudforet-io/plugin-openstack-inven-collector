from spaceone.inventory.manager.resources.metadata.cloud_service_type.share import CST_SHARE_META
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.view.cloud_service import CloudServiceMeta
from spaceone.inventory.model.view.dynamic_field import TextDyField, DateTimeDyField, BadgeDyField, EnumDyField
from spaceone.inventory.model.view.dynamic_layout import ItemDynamicLayout, TableDynamicLayout

CS_SHARE_META = CSTMetaGenerator(CST_SHARE_META)

CS_SHARE_META.insert_cst_meta_field('ID', TextDyField, 'Description', 'data.description')
CS_SHARE_META.insert_cst_meta_field('Size', TextDyField, 'Size', 'data.size', type="size",
                                    options={"source_unit": "KB", "display_unit": "KB"} )
CS_SHARE_META.append_cst_meta_field(TextDyField, 'selfLink', 'data.reference.self_link')
CS_SHARE_META.append_cst_meta_field(TextDyField, 'bookmarkLink', 'data.reference.bookmark_link')
CS_SHARE_META.append_cst_meta_field(TextDyField, 'externalLink', 'data.external_link')

CS_SHARE_NET_META = CSTMetaGenerator()

CS_SHARE_NET_META.append_cst_meta_field(TextDyField, 'ID', 'id')
CS_SHARE_NET_META.append_cst_meta_field(TextDyField, 'Name', 'name')
CS_SHARE_NET_META.append_cst_meta_field(TextDyField, 'Description', 'description')
CS_SHARE_NET_META.append_cst_meta_field(TextDyField, 'CIDR', 'cidr')
CS_SHARE_NET_META.append_cst_meta_field(EnumDyField, 'IP Version', 'ip_version',
                                        default_badge={'coral.600': ['4'], 'indigo.500': ['6']})
CS_SHARE_NET_META.append_cst_meta_field(TextDyField, 'Type', 'network_type')
CS_SHARE_NET_META.append_cst_meta_field(BadgeDyField, 'Network ID', 'neutron_net_id',
                                        reference={"resource_type": "inventory.CloudService",
                                                   "reference_key": "reference.resource_id"})
CS_SHARE_NET_META.append_cst_meta_field(TextDyField, 'Subnet ID', 'neutron_subnet_id')
CS_SHARE_NET_META.append_cst_meta_field(TextDyField, 'Segment ID', 'segmentation_id')
CS_SHARE_NET_META.append_cst_meta_field(DateTimeDyField, 'Created', 'created_at')
CS_SHARE_NET_META.append_cst_meta_field(DateTimeDyField, 'Updated', 'updated_at')

#  Compute
CLOUD_SERVICE_BASE = ItemDynamicLayout.set_fields('Share', fields=CS_SHARE_META.fields)
CLOUD_SERVICE_SHARE_NET = ItemDynamicLayout.set_fields('Network', root_path="data.share_network",
                                                       fields=CS_SHARE_NET_META.get_table_fields())

CLOUD_SERVICE_METADATA = CloudServiceMeta.set_layouts(layouts=[CLOUD_SERVICE_BASE, CLOUD_SERVICE_SHARE_NET])
