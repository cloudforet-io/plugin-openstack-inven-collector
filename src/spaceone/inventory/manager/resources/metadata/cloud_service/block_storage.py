from spaceone.inventory.model.view.dynamic_field import TextDyField, ListDyField, BadgeDyField, DateTimeDyField, \
    EnumDyField, SizeField
from spaceone.inventory.model.view.dynamic_layout import ItemDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.model.view.cloud_service import CloudServiceMeta

#  Compute
CLOUD_SERVICE_BASE = ItemDynamicLayout.set_fields('Volume', fields=[
    TextDyField.data_source('ID', 'data.id'),
    EnumDyField.data_source('State', 'data.status', default_state={
        'safe': ['ACTIVE'],
        'available': ['BUILD', 'PAUSED'],
        'warning': ['MIGRATING', 'HARD_REBOOT', 'PASSWORD', 'REBOOT', 'REBUILD', 'RESCUE', 'SHUTOFF', 'SUSPENDED'],
        'disable': ['DELETED'],
        'alert': ['ERROR']
    }),
    TextDyField.data_source('Size(GB)', 'data.size'),
    TextDyField.data_source('Type', 'data.volume_type'),
    TextDyField.data_source('Multiattached', 'data.multiattach'),
    TextDyField.data_source('Attached', 'data.attachments'),
    TextDyField.data_source('Availability Zone', 'data.availability_zone'),
    TextDyField.data_source('Bootable', 'data.is_bootable'),
    TextDyField.data_source('Source Volume ID', 'data.source_volume_id'),
    TextDyField.data_source('Image Info', 'data.volume_image_metadata'),
    DateTimeDyField.data_source('Encrypted', 'data.is_encrypted '),
    DateTimeDyField.data_source('Created', 'data.created_at'),
    DateTimeDyField.data_source('Updated', 'data.updated_at', options={'is_optional': True})
])

CLOUD_SERVICE_TAGS = SimpleTableDynamicLayout.set_tags()
CLOUD_SERVICE_METADATA = CloudServiceMeta.set_layouts(layouts=[CLOUD_SERVICE_BASE, CLOUD_SERVICE_TAGS])
