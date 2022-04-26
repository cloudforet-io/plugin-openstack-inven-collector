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
    TextDyField.data_source('Availablity Zone', 'dara.reference.ex'),
    ListDyField.data_source('Volumes', 'data.attached_volumes'),
    ListDyField.data_source('Security Groups', 'data.security_groups'),
    DateTimeDyField.data_source('Created', 'data.create_time')
])

CLOUD_SERVICE_TAGS = SimpleTableDynamicLayout.set_tags()
CLOUD_SERVICE_METADATA = CloudServiceMeta.set_layouts(layouts=[CLOUD_SERVICE_BASE, CLOUD_SERVICE_TAGS])
