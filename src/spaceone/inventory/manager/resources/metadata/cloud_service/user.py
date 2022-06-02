from spaceone.inventory.model.view.dynamic_field import TextDyField
from spaceone.inventory.model.view.dynamic_layout import ItemDynamicLayout
from spaceone.inventory.model.view.cloud_service import CloudServiceMeta
from spaceone.inventory.manager.resources.metadata.cloud_service_type.user import CST_USER_META
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator

CS_USER_META = CSTMetaGenerator(CST_USER_META)
CS_USER_META.append_cst_meta_field(TextDyField, 'selfLink', 'data.reference.self_link')
CS_USER_META.append_cst_meta_field(TextDyField, 'externalLink', 'data.external_link')

CLOUD_SERVICE_BASE = ItemDynamicLayout.set_fields('User', fields=CS_USER_META.fields)
CLOUD_SERVICE_METADATA = CloudServiceMeta.set_layouts(layouts=[CLOUD_SERVICE_BASE])
