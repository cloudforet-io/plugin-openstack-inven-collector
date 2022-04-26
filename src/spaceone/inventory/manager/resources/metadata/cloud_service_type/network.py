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
CLOUD_SERVICE_TYPE.name = 'Network'
CLOUD_SERVICE_TYPE.group = 'Compute'
CLOUD_SERVICE_TYPE.labels = ['Compute', 'Network']
CLOUD_SERVICE_TYPE.is_primary = True
CLOUD_SERVICE_TYPE.is_major = True
CLOUD_SERVICE_TYPE.service_code = 'OSNetwork'
CLOUD_SERVICE_TYPE.tags = {
    'spaceone:icon': 'https://wiki.openstack.org/w/images/2/2c/Nova-complete-300.svg',
    'spaceone:display_name': 'Network'
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
        TextDyField.data_source('Flavor', 'data.flavor.name'),
        TextDyField.data_source('IP Address', 'data.addresses'),
        TextDyField.data_source('Key Name', 'data.key_name'),
        TextDyField.data_source('Availablity Zone', 'data.availability_zone'),
        ListDyField.data_source('Volumes', 'data.attached_volumes'),
        ListDyField.data_source('Security Groups', 'data.security_groups'),
        DateTimeDyField.data_source('Created', 'data.create_time')
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

