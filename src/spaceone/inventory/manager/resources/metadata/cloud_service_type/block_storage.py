import os
from spaceone.inventory.libs import common_parser
from spaceone.inventory.model.view.dynamic_widget import ChartWidget, CardWidget
from spaceone.inventory.model.view.dynamic_field import TextDyField, EnumDyField, SearchField, DateTimeDyField, \
    SizeField, ListDyField
from spaceone.inventory.model.common.response import CloudServiceTypeResource, CloudServiceTypeResponse
from spaceone.inventory.model.view.cloud_service_type import CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

"""
VOLUME

vol_total_count_conf = os.path.join(current_dir, 'widget/vol_total_count.yaml')
vol_total_size_conf = os.path.join(current_dir, 'widget/vol_total_size.yaml')
vol_total_size_by_region_conf = os.path.join(current_dir, 'widget/vol_total_size_by_region.yaml')
vol_total_size_by_account_conf = os.path.join(current_dir, 'widget/vol_total_size_by_account.yaml')
vol_total_size_by_az_conf = os.path.join(current_dir, 'widget/vol_total_size_by_az.yaml')
vol_total_size_by_type_conf = os.path.join(current_dir, 'widget/vol_total_size_by_type.yaml')
vol_total_size_by_state_conf = os.path.join(current_dir, 'widget/vol_total_size_by_state.yaml')
"""
CLOUD_SERVICE_TYPE = CloudServiceTypeResource()
CLOUD_SERVICE_TYPE.provider = 'openstack'
CLOUD_SERVICE_TYPE.name = 'Volume'
CLOUD_SERVICE_TYPE.group = 'Storage'
CLOUD_SERVICE_TYPE.labels = ['Compute', 'Volume']
CLOUD_SERVICE_TYPE.is_primary = True
CLOUD_SERVICE_TYPE.is_major = True
CLOUD_SERVICE_TYPE.service_code = 'OSBlockStorage'
CLOUD_SERVICE_TYPE.tags = {
    'spaceone:icon': 'https://wiki.openstack.org/wiki/File:Swift-complete-300.svg',
    'spaceone:display_name': 'BlockStorage'
}
CLOUD_SERVICE_TYPE._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('ID', 'data.id'),
        EnumDyField.data_source('State', 'data.status', default_state={
            'safe': ['ACTIVE'],
            'available': ['BUILD', 'PAUSED'],
            'warning': ['MIGRATING', 'HARD_REBOOT', 'PASSWORD', 'REBOOT', 'REBUILD', 'RESCUE', 'SHUTOFF', 'SUSPENDED'],
            'disable': ['DELETED'],
            'alert': ['ERROR']
        }),
        TextDyField.data_source('Size(GB)', 'data.size'),
        TextDyField.data_source('Image', 'data.volume_image_metadata.image_name'),
        TextDyField.data_source('Type', 'data.volume_type'),
        TextDyField.data_source('Multiattach', 'data.multiattach'),
        TextDyField.data_source('Attached', 'data.attachments'),
        TextDyField.data_source('Availability Zone', 'data.availability_zone'),
        TextDyField.data_source('Bootable', 'data.is_bootable'),
        TextDyField.data_source('Source Volume ID', 'data.source_volume_id'),
        TextDyField.data_source('Host', 'data.host'),
        DateTimeDyField.data_source('Encrypted', 'data.is_encrypted'),
        DateTimeDyField.data_source('Created', 'data.created_at'),
        DateTimeDyField.data_source('Updated', 'data.updated_at')
    ],
    search=[
        SearchField.set(name='ID', key='data.id'),
        SearchField.set(name='Name', key='data.name'),
        SearchField.set(name='Flavor', key='data.flavor.name', data_type='string'),
        SearchField.set(name='State', key='data.status',
                        enums={
                            'ACTIVE': {'label': 'ACTIVE', 'icon': {'color': 'green.500'}},
                            'available': {'label': 'available', 'icon': {'color': 'blue.400'}},
                            'deleting': {'label': 'deleting', 'icon': {'color': 'yellow.500'}},
                            'creating': {'label': 'creating', 'icon': {'color': 'yellow.500'}},
                            'DELETED': {'label': 'DELETED', 'icon': {'color': 'gray.400'}},
                            'ERROR': {'label': 'ERROR', 'icon': {'color': 'red.500'}},
                        }),
        SearchField.set(name='Availability Zone', key='data.availability_zone')
    ],
)
"""
    widget=[
        CardWidget.set(**get_data_from_yaml(vol_total_count_conf)),
        CardWidget.set(**get_data_from_yaml(vol_total_size_conf)),
        ChartWidget.set(**get_data_from_yaml(vol_total_size_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(vol_total_size_by_account_conf)),
        ChartWidget.set(**get_data_from_yaml(vol_total_size_by_az_conf)),
        ChartWidget.set(**get_data_from_yaml(vol_total_size_by_type_conf)),
        ChartWidget.set(**get_data_from_yaml(vol_total_size_by_state_conf))
    ]
)    
   """

