from spaceone.inventory.manager.resources.metadata.cloud_service_type.snapshot import CST_SNAPSHOT_META
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.view.cloud_service import CloudServiceMeta
from spaceone.inventory.model.view.dynamic_field import TextDyField
from spaceone.inventory.model.view.dynamic_layout import ItemDynamicLayout

CS_SNAPSHOT_META = CSTMetaGenerator(CST_SNAPSHOT_META)
CS_SNAPSHOT_META.insert_cst_meta_field('ID', TextDyField, 'Description', 'data.description')
CS_SNAPSHOT_META.insert_cst_meta_field('Size', TextDyField, 'Size (Bytes)', 'data.size', type="size",
                                       options={"display_unit": "BYTES"})

CLOUD_SERVICE_BASE = ItemDynamicLayout.set_fields('Snapshot', fields=CS_SNAPSHOT_META.fields)

CLOUD_SERVICE_METADATA = CloudServiceMeta.set_layouts(layouts=[CLOUD_SERVICE_BASE])
