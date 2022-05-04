from spaceone.inventory.model.view.dynamic_field import TextDyField
from spaceone.inventory.model.view.dynamic_layout import ItemDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.model.view.cloud_service import CloudServiceMeta
from spaceone.inventory.manager.resources.metadata.cloud_service_type.compute import CST_INSTANCE_META

fields = CST_INSTANCE_META.fields.copy()
fields.append(TextDyField.data_source('selfLink', 'data.reference.self_link'))
fields.append(TextDyField.data_source('bookmarkLink', 'data.reference.bookmark_link'))
fields.append(TextDyField.data_source('externalLink', 'data.external_link'))

CLOUD_SERVICE_BASE = ItemDynamicLayout.set_fields('Instance', fields=fields)
CLOUD_SERVICE_TAGS = SimpleTableDynamicLayout.set_tags()
CLOUD_SERVICE_METADATA = CloudServiceMeta.set_layouts(layouts=[CLOUD_SERVICE_BASE, CLOUD_SERVICE_TAGS])
