from spaceone.inventory.manager.resources.metadata.cloud_service.security_group import CS_SG_RULES_META
from spaceone.inventory.manager.resources.metadata.cloud_service_type.block_storage import CST_VOLUME_META
from spaceone.inventory.manager.resources.metadata.cloud_service_type.compute import CST_INSTANCE_META
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.view.cloud_service import CloudServiceMeta
from spaceone.inventory.model.view.dynamic_field import TextDyField, BadgeDyField, EnumDyField, ListDyField, \
    DateTimeDyField
from spaceone.inventory.model.view.dynamic_layout import ItemDynamicLayout, SimpleTableDynamicLayout, TableDynamicLayout

CS_INSTANCE_META = CSTMetaGenerator(CST_INSTANCE_META)

CS_INSTANCE_META.insert_cst_meta_field('ID', TextDyField, 'Description', 'data.description')
CS_INSTANCE_META.append_cst_meta_field(TextDyField, 'Metadata', 'data.metadata')
CS_INSTANCE_META.append_cst_meta_field(TextDyField, 'selfLink', 'data.reference.self_link')
CS_INSTANCE_META.append_cst_meta_field(TextDyField, 'bookmarkLink', 'data.reference.bookmark_link')
CS_INSTANCE_META.append_cst_meta_field(TextDyField, 'externalLink', 'data.external_link')

CLOUD_SERVICE_BASE = ItemDynamicLayout.set_fields('Instance', fields=CS_INSTANCE_META.fields)

CLOUD_SERVICE_INSTANCE_VOLUME = TableDynamicLayout.set_fields('Volumes', root_path='data.volumes',
                                                              fields=CST_VOLUME_META.get_table_fields(
                                                                  ignore_root_path='data'))

CLOUD_SERVICE_INSTANCE_NIC = SimpleTableDynamicLayout.set_fields('Nics', root_path='data.addresses',
                                                                 fields=[
                                                                     TextDyField.data_source('Name', 'network_name'),
                                                                     TextDyField.data_source('Mac', 'mac_addr'),
                                                                     TextDyField.data_source('Type', 'type'),
                                                                     TextDyField.data_source('IP Address', 'addr'),
                                                                     TextDyField.data_source('Version', 'version'),
                                                                 ])

CLOUD_SERVICE_INSTANCE_SG_RULES = TableDynamicLayout.set_fields('Security Groups',
                                                                root_path="data.security_group_rules",
                                                                fields=CS_SG_RULES_META.fields)

CLOUD_SERVICE_METADATA = CloudServiceMeta.set_layouts(layouts=[CLOUD_SERVICE_BASE, CLOUD_SERVICE_INSTANCE_VOLUME,
                                                               CLOUD_SERVICE_INSTANCE_NIC,
                                                               CLOUD_SERVICE_INSTANCE_SG_RULES, ])

# to use the cloud service of other resource
CS_INSTANCES_META = CSTMetaGenerator()
CS_INSTANCES_META.append_cst_meta_field(TextDyField, 'Name', 'name')
CS_INSTANCES_META.append_cst_meta_field(TextDyField, 'Instance Name', 'instance_name')
CS_INSTANCES_META.append_cst_meta_field(BadgeDyField, 'ID', 'id',
                                        reference={"resource_type": "inventory.CloudService",
                                                   "reference_key": "reference.resource_id"}, )
CS_INSTANCES_META.append_cst_meta_field(EnumDyField, 'Status', 'status',
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
CS_INSTANCES_META.append_cst_meta_field(TextDyField, 'Flavor', 'flavor.name')
CS_INSTANCES_META.append_cst_meta_field(TextDyField, 'vCpu', 'flavor.vcpus')
CS_INSTANCES_META.append_cst_meta_field(TextDyField, 'Memory', 'flavor.ram', type="size",
                                        options={"source_unit": "MB"})
CS_INSTANCES_META.append_cst_meta_field(TextDyField, 'Disk Size', 'flavor.disk', type="size",
                                        options={"source_unit": "GB", "display_unit": "GB"})
CS_INSTANCES_META.append_cst_meta_field(ListDyField, 'IP Address', 'addresses.addr')
CS_INSTANCES_META.append_cst_meta_field(TextDyField, 'Availability Zone', 'availability_zone')
CS_INSTANCES_META.append_cst_meta_field(TextDyField, 'Host Name', 'hypervisor_name')
CS_INSTANCES_META.append_cst_meta_field(TextDyField, 'Project Name', 'project_name')
CS_INSTANCES_META.append_cst_meta_field(TextDyField, 'Project ID', 'project_id')
CS_INSTANCES_META.append_cst_meta_field(DateTimeDyField, 'Created', 'created_at')
CS_INSTANCES_META.append_cst_meta_field(DateTimeDyField, 'Updated', 'updated_at')
