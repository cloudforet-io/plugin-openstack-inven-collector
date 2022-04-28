from spaceone.inventory.model.view.dynamic_field import TextDyField, ListDyField, BadgeDyField, DateTimeDyField, \
    EnumDyField, SizeField
from spaceone.inventory.model.view.dynamic_layout import ItemDynamicLayout, SimpleTableDynamicLayout
from spaceone.inventory.model.view.cloud_service import CloudServiceMeta

#  Compute
CLOUD_SERVICE_BASE = ItemDynamicLayout.set_fields('Instance', fields=[
    TextDyField.data_source('ID', 'data.id'),
    EnumDyField.data_source('State', 'data.status', default_state={
        'safe': ['ACTIVE'],
        'available': ['BUILD', 'PAUSED'],
        'warning': ['MIGRATING', 'HARD_REBOOT', 'PASSWORD', 'REBOOT', 'REBUILD', 'RESCUE', 'SHUTOFF', 'SUSPENDED'],
        'disable': ['DELETED'],
        'alert': ['ERROR']
    }),
    TextDyField.data_source('Flavor', 'data.flavor.name'),
    TextDyField.data_source('IP Address', 'data.addresses'),
    TextDyField.data_source('Key Name', 'data.key_name'),
    TextDyField.data_source('Availablity Zone', 'data.availability_zone'),
    ListDyField.data_source('Attached Volumes', 'data.attached_volumes'),
    ListDyField.data_source('Volumes', 'data.volumes.id', reference={"resource_type": "inventory.CloudService",
                            "reference_key": "reference.resource_id"}),
    ListDyField.data_source('Security Groups', 'data.security_groups'),
    DateTimeDyField.data_source('Created', 'data.created_at'),
    DateTimeDyField.data_source('Updated', 'data.updated_at'),
    TextDyField.data_source('selfLink', 'data.reference.self_link'),
    TextDyField.data_source('bookmarkLink', 'data.reference.bookmark_link'),
    TextDyField.data_source('ExternalLink', 'data.reference.external_link'),
])

CLOUD_SERVICE_TAGS = SimpleTableDynamicLayout.set_tags()
CLOUD_SERVICE_METADATA = CloudServiceMeta.set_layouts(layouts=[CLOUD_SERVICE_BASE, CLOUD_SERVICE_TAGS])
