from spaceone.inventory.manager.resources.metadata.cloud_service.compute import CS_INSTANCES_META
from spaceone.inventory.manager.resources.metadata.cloud_service_type.server_group import CST_SG_META
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.view.cloud_service import CloudServiceMeta
from spaceone.inventory.model.view.dynamic_field import TextDyField
from spaceone.inventory.model.view.dynamic_layout import ItemDynamicLayout, TableDynamicLayout

CS_SG_META = CSTMetaGenerator(CST_SG_META)
CS_SG_META.append_cst_meta_field(TextDyField, 'Policies', 'data.policies')
CS_SG_META.append_cst_meta_field(TextDyField, 'Metadata', 'data.metadata')
CS_SG_META.append_cst_meta_field(TextDyField, 'Rules', 'data.rules')

CLOUD_SERVICE_BASE = ItemDynamicLayout.set_fields('Server Group', fields=CS_SG_META.fields)

CS_SG_INSTANCE_META = CSTMetaGenerator(CS_INSTANCES_META)

CLOUD_SERVICE_SG_INSTANCES = TableDynamicLayout.set_fields('Instances', root_path="data.instances",
                                                           fields=CS_SG_INSTANCE_META.get_table_fields())

CLOUD_SERVICE_METADATA = CloudServiceMeta.set_layouts(layouts=[CLOUD_SERVICE_BASE, CLOUD_SERVICE_SG_INSTANCES])
