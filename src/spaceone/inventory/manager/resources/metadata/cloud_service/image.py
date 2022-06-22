from spaceone.inventory.manager.resources.metadata.cloud_service_type.image import CST_IMAGE_META
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.view.cloud_service import CloudServiceMeta
from spaceone.inventory.model.view.dynamic_layout import ItemDynamicLayout

CS_IMAGE_META = CSTMetaGenerator(CST_IMAGE_META)
CS_IMAGE_META.append_cst_meta_field('TextDyField', 'ID', 'data.id', index=0)
CS_IMAGE_META.insert_cst_meta_field('ID', 'TextDyField', 'Name', 'data.name')
CS_IMAGE_META.insert_cst_meta_field('Name', 'TextDyField', 'Description', 'data.description')
CS_IMAGE_META.insert_cst_meta_field('Protected', 'TextDyField', 'Metadata', 'data.metadata')
CS_IMAGE_META.insert_cst_meta_field('Protected', 'DictDyField', 'Properties', 'data.properties')
CS_IMAGE_META.insert_cst_meta_field('Protected', 'TextDyField', 'Min Disk', 'data.min_disk')
CS_IMAGE_META.insert_cst_meta_field('Protected', 'TextDyField', 'Min Ram', 'data.min_ram')
CS_IMAGE_META.insert_cst_meta_field('Protected', 'TextDyField', 'Checksum', 'data.checksum')
CS_IMAGE_META.insert_cst_meta_field('Protected', 'TextDyField', 'Hash', 'data.hash_algo')
CS_IMAGE_META.insert_cst_meta_field('Protected', 'TextDyField', 'File', 'data.file')
CS_IMAGE_META.insert_cst_meta_field('Size', 'TextDyField', 'Size (Bytes)', 'data.size', type="size",
                                    options={"display_unit": "BYTES"})

CLOUD_SERVICE_BASE = ItemDynamicLayout.set_fields('Image', fields=CS_IMAGE_META.fields)

CLOUD_SERVICE_METADATA = CloudServiceMeta.set_layouts(layouts=[CLOUD_SERVICE_BASE])
