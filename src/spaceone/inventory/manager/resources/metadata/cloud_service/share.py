from spaceone.inventory.manager.resources.metadata.cloud_service_type.share import CST_SHARE_META
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.view.cloud_service import CloudServiceMeta
from spaceone.inventory.model.view.dynamic_field import TextDyField
from spaceone.inventory.model.view.dynamic_layout import ItemDynamicLayout

CS_VOLUME_META = CSTMetaGenerator(CST_SHARE_META)

CS_VOLUME_META.insert_cst_meta_field('ID', TextDyField, 'Description', 'data.description')
CS_VOLUME_META.insert_cst_meta_field('Size(GiB)', TextDyField, 'Size(Byte)', 'data.size')
CS_VOLUME_META.append_cst_meta_field(TextDyField, 'selfLink', 'data.reference.self_link')
CS_VOLUME_META.append_cst_meta_field(TextDyField, 'bookmarkLink', 'data.reference.bookmark_link')
CS_VOLUME_META.append_cst_meta_field(TextDyField, 'externalLink', 'data.external_link')

#  Compute
CLOUD_SERVICE_BASE = ItemDynamicLayout.set_fields('Share', fields=CS_VOLUME_META.fields)

CLOUD_SERVICE_METADATA = CloudServiceMeta.set_layouts(layouts=[CLOUD_SERVICE_BASE])
