from spaceone.inventory.manager.resources.metadata.cloud_service_type.router import CST_ROUTER_META
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.view.cloud_service import CloudServiceMeta
from spaceone.inventory.model.view.dynamic_field import TextDyField, EnumDyField, ListDyField
from spaceone.inventory.model.view.dynamic_layout import ItemDynamicLayout

CS_ROUTER_META = CSTMetaGenerator(CST_ROUTER_META)
CS_ROUTER_META.insert_cst_meta_field('ID', TextDyField, 'Description', 'data.description')
CS_ROUTER_META.insert_cst_meta_field('External G/W Network ID', TextDyField, 'External Gateway Info',
                                     'data.external_gateway_info')
CS_ROUTER_META.insert_cst_meta_field('Admin Status', EnumDyField, 'Distributed', 'data.is_distributed',
                                     default_badge={
                                         'green.500': ['true'], 'red.600': ['false']
                                     })
CS_ROUTER_META.insert_cst_meta_field('Distributed', EnumDyField, 'HA', 'data.is_ha',
                                     default_badge={
                                         'green.500': ['true'], 'red.600': ['false']
                                     })
CS_ROUTER_META.insert_cst_meta_field('Availability Zones', ListDyField, 'Availability Zone Hints',
                                     'data.availability_zone_hints')
CS_ROUTER_META.insert_cst_meta_field('External Gateway Info', ListDyField, 'Routes', 'data.routes')

CLOUD_SERVICE_BASE = ItemDynamicLayout.set_fields('Router', fields=CS_ROUTER_META.fields)

CLOUD_SERVICE_METADATA = CloudServiceMeta.set_layouts(layouts=[CLOUD_SERVICE_BASE])
