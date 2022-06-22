from spaceone.inventory.manager.resources.metadata.cloud_service.security_group import CS_SG_RULES_META
from spaceone.inventory.manager.resources.metadata.cloud_service_type.block_storage import CST_VOLUME_META
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.view.cloud_service import CloudServiceMeta
from spaceone.inventory.model.view.dynamic_field import TextDyField
from spaceone.inventory.model.view.dynamic_layout import ListDynamicLayout, SimpleTableDynamicLayout, \
    TableDynamicLayout, ItemDynamicLayout


CS_INSTANCE_DETAIL_META = CSTMetaGenerator()

CS_INSTANCE_DETAIL_META.append_cst_meta_field('BadgeDyField', 'ID', 'data.id',
                                              reference={"resource_type": "inventory.CloudService",
                                                         "reference_key": "reference.resource_id"})
CS_INSTANCE_DETAIL_META.append_cst_meta_field('TextDyField', 'Name', 'data.name')
CS_INSTANCE_DETAIL_META.append_cst_meta_field('TextDyField', 'Description', 'data.description')
CS_INSTANCE_DETAIL_META.append_cst_meta_field('TextDyField', 'Host Name', 'data.hostname')
CS_INSTANCE_DETAIL_META.append_cst_meta_field('TextDyField', 'Instance Name', 'data.instance_name')
CS_INSTANCE_DETAIL_META.append_cst_meta_field('EnumDyField', 'Status', 'data.status',
                                              default_state={
                                                  'safe': ['ACTIVE'],
                                                  'available': ['BUILD', 'PAUSED'],
                                                  'warning': ['HARD_REBOOT', 'MIGRATING', 'PASSWORD', 'REBOOT',
                                                              'REBUILD',
                                                              'RESCUE', 'RESIZE', 'REVERT_RESIZE', 'SHELVED',
                                                              'VERIFY_RESIZE'],
                                                  'disable': ['SOFT_DELETED', 'PAUSED', 'DELETED', 'SUSPENDED',
                                                              'SHUTOFF'],
                                                  'alert': ['ERROR', 'UNKNOWN']}
                                              )
CS_INSTANCE_DETAIL_META.append_cst_meta_field('EnumDyField', 'VM State', 'data.vm_state',
                                              default_state={
                                                  'safe': ['ACTIVE'],
                                                  'available': ['BUILD', 'RESCUED', 'RESIZED', 'SHELVED',
                                                                'SHELVED_OFFLOADED'],
                                                  'warning': ['BUILDING'],
                                                  'disable': ['DELETED', 'PAUSED', 'SOFT_DELETED', 'STOPPED',
                                                              'SUSPENDED'],
                                                  'alert': ['ERROR']}
                                              )

CS_INSTANCE_DETAIL_META.append_cst_meta_field('ListDyField', 'IP Address', 'data.addresses',
                                              options={'delimiter': ', ', 'sub_key': 'addr'})
CS_INSTANCE_DETAIL_META.append_cst_meta_field('ListDyField', 'Network Name', 'data.addresses',
                                              options={'delimiter': ', ', 'sub_key': 'network_name'})
CS_INSTANCE_DETAIL_META.append_cst_meta_field('TextDyField', 'Key Name', 'data.key_name')
CS_INSTANCE_DETAIL_META.append_cst_meta_field('ListDyField', 'Security Groups', 'data.security_groups',
                                              options={'delimiter': ', ', 'sub_key': 'name'})
CS_INSTANCE_DETAIL_META.append_cst_meta_field('DictDyField', 'Metadata', 'data.metadata')
CS_INSTANCE_DETAIL_META.append_cst_meta_field('TextDyField', 'Availability Zone', 'data.availability_zone')
CS_INSTANCE_DETAIL_META.append_cst_meta_field('TextDyField', 'Project Name', 'data.project_name')
CS_INSTANCE_DETAIL_META.append_cst_meta_field('BadgeDyField', 'Project ID', 'data.project_id',
                                              reference={"resource_type": "inventory.CloudService",
                                                         "reference_key": "reference.resource_id"})
CS_INSTANCE_DETAIL_META.append_cst_meta_field('BadgeDyField', 'User ID', 'data.user_id',
                                              reference={"resource_type": "inventory.CloudService",
                                                         "reference_key": "reference.resource_id"})
CS_INSTANCE_DETAIL_META.append_cst_meta_field('DateTimeDyField', 'Created', 'data.created_at')
CS_INSTANCE_DETAIL_META.append_cst_meta_field('DateTimeDyField', 'Updated', 'data.updated_at')
CS_INSTANCE_DETAIL_META.append_cst_meta_field('TextDyField', 'selfLink', 'data.reference.self_link')
CS_INSTANCE_DETAIL_META.append_cst_meta_field('TextDyField', 'bookmarkLink', 'data.reference.bookmark_link')
CS_INSTANCE_DETAIL_META.append_cst_meta_field('TextDyField', 'externalLink', 'data.external_link')

# FLAVOR
CS_INSTANCE_FLAVOR_META = CSTMetaGenerator()

CS_INSTANCE_FLAVOR_META.append_cst_meta_field('TextDyField', 'Flavor Name', 'data.flavor.name')
CS_INSTANCE_FLAVOR_META.append_cst_meta_field('TextDyField', 'vCPU', 'data.flavor.vcpus', data_type=int)
CS_INSTANCE_FLAVOR_META.append_cst_meta_field('TextDyField', 'Memory', 'data.flavor.ram', data_type=int,
                                              type="size", options={"source_unit": "MB"})

# VOLUME
CS_INSTANCE_VOLUME_META = CSTMetaGenerator()

CS_INSTANCE_VOLUME_META.append_cst_meta_field('ListDyField', 'Volume ID', 'data.volumes',
                                              reference={"resource_type": "inventory.CloudService",
                                                         "reference_key": "reference.resource_id"},
                                              default_badge={"type": "reference", 'delimiter': ' ', 'sub_key': 'id'}
                                              )
CS_INSTANCE_VOLUME_META.append_cst_meta_field('TextDyField', 'Volume Count', 'data.volume_count', data_type=int)
CS_INSTANCE_VOLUME_META.append_cst_meta_field('TextDyField', 'Total Volume Size', 'data.total_volume_size', data_type=int,
                                              type="size", options={"source_unit": "GB", "display_unit": "GB"}
                                              )
CS_INSTANCE_VOLUME_META.append_cst_meta_field('TextDyField', 'Image Name', 'data.image_name',
                                              associated_resource=True)
CS_INSTANCE_VOLUME_META.append_cst_meta_field('BadgeDyField', 'Image ID', 'data.image_id',
                                              reference={"resource_type": "inventory.CloudService",
                                                         "reference_key": "reference.resource_id"},
                                              )

# HYPERVISOR
CS_INSTANCE_HYPERVISOR_META = CSTMetaGenerator()

CS_INSTANCE_HYPERVISOR_META.append_cst_meta_field('TextDyField', 'Hypervisor Name', 'data.hypervisor_name')
CS_INSTANCE_HYPERVISOR_META.append_cst_meta_field('BadgeDyField', 'Hypervisor ID', 'data.hypervisor_id',
                                                  reference={"resource_type": "inventory.CloudService",
                                                             "reference_key": "reference.resource_id"},
                                                  )


CS_INSTANCE_DETAIL = ItemDynamicLayout.set_fields('Details', fields=CS_INSTANCE_DETAIL_META.fields)
CS_INSTANCE_FLAVOR = ItemDynamicLayout.set_fields('Flavor', fields=CS_INSTANCE_FLAVOR_META.fields)
CS_INSTANCE_VOLUME = ItemDynamicLayout.set_fields('Volume', fields=CS_INSTANCE_VOLUME_META.fields)
CS_INSTANCE_HYPERVISOR = ItemDynamicLayout.set_fields('Hypervisor', fields=CS_INSTANCE_HYPERVISOR_META.fields)

CLOUD_SERVICE_BASE = ListDynamicLayout.set_layouts('Instance', layouts=[CS_INSTANCE_DETAIL, CS_INSTANCE_FLAVOR,
                                                                        CS_INSTANCE_VOLUME, CS_INSTANCE_HYPERVISOR])

CLOUD_SERVICE_INSTANCE_VOLUME = TableDynamicLayout.set_fields('Volumes', root_path='data.volumes',
                                                              fields=CST_VOLUME_META.get_table_fields(
                                                                  ignore_data_path=True))

CLOUD_SERVICE_INSTANCE_NIC = SimpleTableDynamicLayout.set_fields('Nics', root_path='data.addresses',
                                                                 fields=[
                                                                     TextDyField.data_source('Network Name', 'network_name'),
                                                                     TextDyField.data_source('Mac', 'mac_addr'),
                                                                     TextDyField.data_source('Type', 'type'),
                                                                     TextDyField.data_source('IP Address', 'addr'),
                                                                     TextDyField.data_source('Version', 'version'),
                                                                 ])

CLOUD_SERVICE_INSTANCE_SG_RULES = TableDynamicLayout.set_fields('Security Group Name',
                                                                root_path="data.security_group_rules",
                                                                fields=CS_SG_RULES_META.fields)

CLOUD_SERVICE_METADATA = CloudServiceMeta.set_layouts(layouts=[CLOUD_SERVICE_BASE, CLOUD_SERVICE_INSTANCE_VOLUME,
                                                               CLOUD_SERVICE_INSTANCE_NIC,
                                                               CLOUD_SERVICE_INSTANCE_SG_RULES, ])

# to use the cloud service of other resource
CS_INSTANCES_META = CSTMetaGenerator()
CS_INSTANCES_META.append_cst_meta_field('TextDyField', 'Name', 'name')
CS_INSTANCES_META.append_cst_meta_field('TextDyField', 'Instance Name', 'instance_name')
CS_INSTANCES_META.append_cst_meta_field('BadgeDyField', 'ID', 'id',
                                        reference={"resource_type": "inventory.CloudService",
                                                   "reference_key": "reference.resource_id"}, )
CS_INSTANCES_META.append_cst_meta_field('EnumDyField', 'Status', 'status',
                                        default_state={
                                            'safe': ['ACTIVE'],
                                            'available': ['BUILD', 'PAUSED'],
                                            'warning': ['HARD_REBOOT', 'MIGRATING', 'PASSWORD', 'REBOOT',
                                                        'REBUILD',
                                                        'RESCUE', 'RESIZE', 'REVERT_RESIZE', 'SHELVED',
                                                        'VERIFY_RESIZE'],
                                            'disable': ['SOFT_DELETED', 'PAUSED', 'DELETED', 'SUSPENDED',
                                                        'SHUTOFF'],
                                            'alert': ['ERROR', 'UNKNOWN']}
                                        )
CS_INSTANCES_META.append_cst_meta_field('TextDyField', 'Flavor Name', 'flavor.name')
CS_INSTANCES_META.append_cst_meta_field('TextDyField', 'vCpu', 'flavor.vcpus')
CS_INSTANCES_META.append_cst_meta_field('TextDyField', 'Memory', 'flavor.ram', type="size",
                                        options={"source_unit": "MB"})
CS_INSTANCES_META.append_cst_meta_field('TextDyField', 'Disk Size', 'flavor.disk', type="size",
                                        options={"source_unit": "GB", "display_unit": "GB"})
CS_INSTANCES_META.append_cst_meta_field('ListDyField', 'IP Address', 'addresses.addr')
CS_INSTANCES_META.append_cst_meta_field('TextDyField', 'Availability Zone', 'availability_zone')
CS_INSTANCES_META.append_cst_meta_field('TextDyField', 'Hypervisor Name', 'hypervisor_name')
CS_INSTANCES_META.append_cst_meta_field('TextDyField', 'Project Name', 'project_name')
CS_INSTANCES_META.append_cst_meta_field('TextDyField', 'Project ID', 'project_id')
CS_INSTANCES_META.append_cst_meta_field('DateTimeDyField', 'Created', 'created_at')
CS_INSTANCES_META.append_cst_meta_field('DateTimeDyField', 'Updated', 'updated_at')
