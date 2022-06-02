from spaceone.inventory.manager.resources.metadata.cloud_service_type.security_group import CST_SG_META
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.view.cloud_service import CloudServiceMeta
from spaceone.inventory.model.view.dynamic_field import TextDyField, DateTimeDyField, \
    EnumDyField, BadgeDyField
from spaceone.inventory.model.view.dynamic_layout import ItemDynamicLayout, TableDynamicLayout

CS_SG_RULES_META = CSTMetaGenerator()

CS_SG_RULES_META.append_cst_meta_field(EnumDyField, 'Direction', 'direction', auto_search=True,
                                       default_badge={'coral.600': ['ingress'], 'indigo.500': ['egress']})
CS_SG_RULES_META.append_cst_meta_field(TextDyField, 'ID', 'id', auto_search=True)
CS_SG_RULES_META.append_cst_meta_field(EnumDyField, 'Type', 'ethertype', auto_search=True,
                                       default_badge={'coral.600': ['IPv4'], 'indigo.500': ['IPv6']})
CS_SG_RULES_META.append_cst_meta_field(TextDyField, 'Start', 'port_range_min', auto_search=True)
CS_SG_RULES_META.append_cst_meta_field(TextDyField, 'End', 'port_range_max', auto_search=True)
CS_SG_RULES_META.append_cst_meta_field(EnumDyField, 'Protocol', 'protocol', auto_search=True,
                                       default_badge={
                                           'coral.600': ['all'], 'indigo.500': ['tcp'], 'peacock.500': ['udp'],
                                           'green.500': ['icmp']})
CS_SG_RULES_META.append_cst_meta_field(TextDyField, 'Remote', 'remote_ip_prefix', auto_search=True)
CS_SG_RULES_META.append_cst_meta_field(TextDyField, 'Security Group Name', 'security_group_name', auto_search=True)
CS_SG_RULES_META.append_cst_meta_field(BadgeDyField, 'Security Group ID', 'security_group_id', auto_search=True,
                                       reference={"resource_type": "inventory.CloudService",
                                                  "reference_key": "reference.resource_id"})
CS_SG_RULES_META.append_cst_meta_field(DateTimeDyField, 'Created', 'created_at', auto_search=True)

CLOUD_SERVICE_BASE = ItemDynamicLayout.set_fields('Security Group', fields=CST_SG_META.fields)
CLOUD_SERVICE_SG_RULES = TableDynamicLayout.set_fields('Rules', root_path="data.security_group_rules",
                                                       fields=CS_SG_RULES_META.fields)

CLOUD_SERVICE_METADATA = CloudServiceMeta.set_layouts(
    layouts=[CLOUD_SERVICE_BASE, CLOUD_SERVICE_SG_RULES])
