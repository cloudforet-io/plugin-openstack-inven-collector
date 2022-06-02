from spaceone.inventory.model.resources.base import ResourceModel
from schematics.types import ModelType, ListType, StringType, IntType, DateTimeType, BooleanType, FloatType, DictType


class ProjectModel(ResourceModel):
    name = StringType()
    description = StringType()
    domain_id = StringType()
    is_domain = BooleanType()
    is_enabled = BooleanType()
    options = StringType()
    parent_id = StringType()
    quota_sets = ListType(DictType(StringType))
