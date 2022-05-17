from spaceone.inventory.manager.resources.metadata.cloud_service_type.compute import CST_INSTANCE_META
from spaceone.inventory.manager.resources.metadata.cloud_service_type.hypervisor import CST_HV_META
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.view.cloud_service import CloudServiceMeta
from spaceone.inventory.model.view.dynamic_layout import ItemDynamicLayout, TableDynamicLayout

CS_HV_META = CSTMetaGenerator(CST_HV_META)

CLOUD_SERVICE_BASE = ItemDynamicLayout.set_fields('Hypervisor', fields=CS_HV_META.fields)

CLOUD_SERVICE_HV_INSTANCE = TableDynamicLayout.set_fields('Instances', root_path="data.instances",
                                                          fields=CST_INSTANCE_META.get_table_fields(ignore_root_path="data",
                                                                                                    ignore_associated_resource=True))

CLOUD_SERVICE_METADATA = CloudServiceMeta.set_layouts(layouts=[CLOUD_SERVICE_BASE, CLOUD_SERVICE_HV_INSTANCE])
