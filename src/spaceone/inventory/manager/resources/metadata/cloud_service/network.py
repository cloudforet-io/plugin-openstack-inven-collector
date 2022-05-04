from spaceone.inventory.model.view.dynamic_field import TextDyField, ListDyField, BadgeDyField, DateTimeDyField, \
    EnumDyField, SizeField
from spaceone.inventory.model.view.dynamic_layout import ItemDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.model.view.cloud_service import CloudServiceMeta

from spaceone.inventory.manager.resources.metadata.cloud_service_type.network import CST_NETWORK_META

fields = CST_NETWORK_META.fields.copy()
fields.append(TextDyField.data_source('externalLink', 'data.external_link'))

CLOUD_SERVICE_BASE = ItemDynamicLayout.set_fields('Network', fields=fields)
CLOUD_SERVICE_TAGS = SimpleTableDynamicLayout.set_tags()
CLOUD_SERVICE_METADATA = CloudServiceMeta.set_layouts(layouts=[CLOUD_SERVICE_BASE, CLOUD_SERVICE_TAGS])
