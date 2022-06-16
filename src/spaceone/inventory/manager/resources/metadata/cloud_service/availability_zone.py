from spaceone.inventory.manager.resources.metadata.cloud_service_type.availability_zone import CST_COMPUTE_ZONE_META
from spaceone.inventory.manager.resources.metadata.cloud_service_type.hypervisor import CST_HV_META
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.view.cloud_service import CloudServiceMeta
from spaceone.inventory.model.view.dynamic_layout import ItemDynamicLayout, TableDynamicLayout

CS_COMPUTE_ZONE_META = CSTMetaGenerator(CST_COMPUTE_ZONE_META)

CLOUD_SERVICE_BASE = ItemDynamicLayout.set_fields('Availability Zone', fields=CS_COMPUTE_ZONE_META.fields)

CS_COMPUTE_ZONE_HV_META = CSTMetaGenerator(CST_HV_META)
CS_COMPUTE_ZONE_HV_META.delete_cst_meta_field("Availability Zone")

CLOUD_SERVICE_HYPERVISOR = TableDynamicLayout.set_fields('Hypervisors', fields=CS_COMPUTE_ZONE_HV_META.get_table_fields(
    ignore_root_path='data'),
                                                         root_path="data.hypervisors")

CLOUD_SERVICE_METADATA = CloudServiceMeta.set_layouts(layouts=[CLOUD_SERVICE_BASE, CLOUD_SERVICE_HYPERVISOR])
