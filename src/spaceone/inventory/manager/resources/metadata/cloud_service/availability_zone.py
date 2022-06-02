from spaceone.inventory.manager.resources.metadata.cloud_service_type.availability_zone import CST_COMPUTE_ZONE_META
from spaceone.inventory.manager.resources.metadata.cloud_service_type.hypervisor import CST_HV_META
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.view.cloud_service import CloudServiceMeta
from spaceone.inventory.model.view.dynamic_field import TextDyField, DateTimeDyField, BadgeDyField
from spaceone.inventory.model.view.dynamic_layout import ItemDynamicLayout, TableDynamicLayout

CS_COMPUTE_ZONE_META = CSTMetaGenerator(CST_COMPUTE_ZONE_META)

CLOUD_SERVICE_BASE = ItemDynamicLayout.set_fields('Availability Zone', fields=CS_COMPUTE_ZONE_META.fields)

CLOUD_SERVICE_HYPERVISOR = TableDynamicLayout.set_fields('Hypervisors', fields=CST_HV_META.get_table_fields(
                                                         ignore_root_path='data'),
                                                         root_path="data.hypervisors")

CLOUD_SERVICE_METADATA = CloudServiceMeta.set_layouts(layouts=[CLOUD_SERVICE_BASE, CLOUD_SERVICE_HYPERVISOR])
