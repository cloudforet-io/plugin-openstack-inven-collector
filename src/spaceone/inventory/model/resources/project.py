from schematics.types import ListType, StringType, BooleanType, DictType

from spaceone.inventory.model.resources.base import ResourceModel


class ProjectModel(ResourceModel):
    name = StringType()
    description = StringType()
    domain_id = StringType()
    is_domain = BooleanType()
    is_enabled = BooleanType()
    options = StringType()
    parent_id = StringType()
    quota_sets = ListType(StringType, default=[])
