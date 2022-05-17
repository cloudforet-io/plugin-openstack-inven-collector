from schematics.types import ModelType, ListType, StringType, IntType, DateTimeType

from spaceone.inventory.model.resources.base import ResourceModel


class SecurityGroupModel(ResourceModel):
    id = StringType()
    name = StringType()
    description = StringType()
    tenant_id = StringType()
    created_at = DateTimeType()
    updated_at = DateTimeType()
    security_group_rules = ListType(ModelType('SecurityGroupRuleModel'), default=[])

class SecurityGroupRuleModel(ResourceModel):
    id = StringType()
    security_group_name = StringType()
    security_group_id = StringType()
    direction = StringType()
    ethertype = StringType()
    port_range_max = IntType()
    port_range_min = IntType()
    protocol = StringType()
    remote_ip_prefix = StringType()
    created_at = DateTimeType()