from spaceone.inventory.manager.resources.metadata.cloud_service_type.subnet import CST_SUBNET_META
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.view.cloud_service import CloudServiceMeta
from spaceone.inventory.model.view.dynamic_layout import ItemDynamicLayout
from spaceone.inventory.model.view.dynamic_field import TextDyField

CS_SUBNET_META = CSTMetaGenerator(CST_SUBNET_META)

CS_SUBNET_META.insert_cst_meta_field('ID', TextDyField, 'Description', 'data.description')

CLOUD_SERVICE_BASE = ItemDynamicLayout.set_fields('Subnet', fields=CS_SUBNET_META.fields)
CLOUD_SERVICE_METADATA = CloudServiceMeta.set_layouts(layouts=[CLOUD_SERVICE_BASE])

