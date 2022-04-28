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
    ListDyField.data_source('Segments', 'data.segments'),
    ListDyField.data_source('Subnet ids', 'data.subnet_ids'),
    TextDyField.data_source('MTU', 'data.mtu'),
    TextDyField.data_source('Availablity Zone', 'data.availability_zone'),
    TextDyField.data_source('Shared', 'data.is_shared'),
    TextDyField.data_source('Vlan Transparent', 'data.vlan_transparent'),
    DateTimeDyField.data_source('Created', 'data.created_at'),
    DateTimeDyField.data_source('Updated', 'data.updated_at')
])

CLOUD_SERVICE_TAGS = SimpleTableDynamicLayout.set_tags()
CLOUD_SERVICE_METADATA = CloudServiceMeta.set_layouts(layouts=[CLOUD_SERVICE_BASE, CLOUD_SERVICE_TAGS])
