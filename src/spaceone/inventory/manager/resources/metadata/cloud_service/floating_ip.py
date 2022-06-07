from spaceone.inventory.manager.resources.metadata.cloud_service_type.floating_ip import CST_FLOATING_IP_META
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.view.cloud_service import CloudServiceMeta
from spaceone.inventory.model.view.dynamic_field import TextDyField
from spaceone.inventory.model.view.dynamic_layout import ItemDynamicLayout

CS_FLOATING_IP_META = CSTMetaGenerator(CST_FLOATING_IP_META)
CS_FLOATING_IP_META.insert_cst_meta_field('ID', TextDyField, 'Description', 'data.description')



CLOUD_SERVICE_BASE = ItemDynamicLayout.set_fields('Floating IP', fields=CS_FLOATING_IP_META.fields)

CLOUD_SERVICE_METADATA = CloudServiceMeta.set_layouts(layouts=[CLOUD_SERVICE_BASE])
