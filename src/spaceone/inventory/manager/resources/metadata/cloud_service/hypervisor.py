from spaceone.inventory.manager.resources.metadata.cloud_service.compute import CS_INSTANCES_META
from spaceone.inventory.manager.resources.metadata.cloud_service_type.hypervisor import CST_HV_META
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.view.cloud_service import CloudServiceMeta
from spaceone.inventory.model.view.dynamic_field import DictDyField
from spaceone.inventory.model.view.dynamic_layout import ItemDynamicLayout, TableDynamicLayout

CS_HV_META = CSTMetaGenerator(CST_HV_META)
CS_HV_META.insert_cst_meta_field('vCPU Model', DictDyField, 'vCPU Topology', 'data.cpu_info.topology')

CLOUD_SERVICE_BASE = ItemDynamicLayout.set_fields('Hypervisor', fields=CS_HV_META.fields)

CS_HV_INSTANCE_META = CSTMetaGenerator(CS_INSTANCES_META)

CLOUD_SERVICE_HV_INSTANCE = TableDynamicLayout.set_fields('Instances', root_path="data.instances",
                                                          fields=CS_HV_INSTANCE_META.get_table_fields())

CLOUD_SERVICE_METADATA = CloudServiceMeta.set_layouts(layouts=[CLOUD_SERVICE_BASE, CLOUD_SERVICE_HV_INSTANCE])
