from spaceone.inventory.manager.resources.metadata.cloud_service_type.hypervisor import CST_HV_META
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.view.cloud_service import CloudServiceMeta
from spaceone.inventory.model.view.dynamic_layout import ItemDynamicLayout, TableDynamicLayout
from spaceone.inventory.model.view.dynamic_field import TextDyField, DateTimeDyField, ListDyField, EnumDyField, BadgeDyField

CS_HV_META = CSTMetaGenerator(CST_HV_META)

CLOUD_SERVICE_BASE = ItemDynamicLayout.set_fields('Hypervisor', fields=CS_HV_META.fields)

CS_HV_INSTANCE_META = CSTMetaGenerator()
CS_HV_INSTANCE_META.append_cst_meta_field(TextDyField, 'Name', 'name')
CS_HV_INSTANCE_META.append_cst_meta_field(TextDyField, 'Instance Name', 'instance_name')
CS_HV_INSTANCE_META.append_cst_meta_field(BadgeDyField, 'ID', 'id',
                                          reference={"resource_type": "inventory.CloudService",
                                                     "reference_key": "reference.resource_id"},)
CS_HV_INSTANCE_META.append_cst_meta_field(EnumDyField, 'Status', 'status',
                                          default_state={
                                              'safe': ['ACTIVE'],
                                              'available': ['BUILD', 'PAUSED'],
                                              'warning': ['HARD_REBOOT', 'MIGRATING', 'PASSWORD', 'REBOOT', 'REBUILD',
                                                          'RESCUE', 'RESIZE', 'REVERT_RESIZE', 'SHELVED',
                                                          'VERIFY_RESIZE'],
                                              'disable': ['SOFT_DELETED', 'PAUSED', 'DELETED', 'SUSPENDED', 'SHUTOFF'],
                                              'alert': ['ERROR', 'UNKNOWN']}
                                          )
CS_HV_INSTANCE_META.append_cst_meta_field(TextDyField, 'Flavor', 'flavor.name')
CS_HV_INSTANCE_META.append_cst_meta_field(TextDyField, 'vCpu', 'flavor.vcpus')
CS_HV_INSTANCE_META.append_cst_meta_field(TextDyField, 'Memory', 'flavor.ram', type="size",
                                          options={"source_unit": "MB"})
CS_HV_INSTANCE_META.append_cst_meta_field(TextDyField, 'Disk Size', 'flavor.disk', type="size",
                                          options={"source_unit": "GB", "display_unit": "GB"})
CS_HV_INSTANCE_META.append_cst_meta_field(ListDyField, 'IP Address', 'addresses.addr')
CS_HV_INSTANCE_META.append_cst_meta_field(TextDyField, 'Availability Zone', 'availability_zone')
CS_HV_INSTANCE_META.append_cst_meta_field(TextDyField, 'Host Name', 'hypervisor_name')
CS_HV_INSTANCE_META.append_cst_meta_field(TextDyField, 'Project Name', 'project_name')
CS_HV_INSTANCE_META.append_cst_meta_field(TextDyField, 'Project ID', 'project_id')
CS_HV_INSTANCE_META.append_cst_meta_field(DateTimeDyField, 'Created', 'created_at')
CS_HV_INSTANCE_META.append_cst_meta_field(DateTimeDyField, 'Updated', 'updated_at')

CLOUD_SERVICE_HV_INSTANCE = TableDynamicLayout.set_fields('Instances', root_path="data.instances",
                                                          fields=CS_HV_INSTANCE_META.get_table_fields())

CLOUD_SERVICE_METADATA = CloudServiceMeta.set_layouts(layouts=[CLOUD_SERVICE_BASE, CLOUD_SERVICE_HV_INSTANCE])
