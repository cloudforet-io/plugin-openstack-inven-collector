from schematics.types import ModelType, StringType, DateTimeType, BooleanType, DictType

from spaceone.inventory.model.resources.base import ResourceModel


class UserModel(ResourceModel):
    name = StringType()
    description = StringType()
    domain_id = StringType()
    default_project_id = StringType()
    email = StringType()
    is_enabled = BooleanType()
    role = ModelType('RoleModel')
    password_expires_at = DateTimeType()

class RoleModel(ResourceModel):
    name = StringType()
    description = StringType()
    domain_id = StringType()

class RoleAssignmentModel(ResourceModel):
    role = DictType(StringType())
    scope = DictType(StringType())
    user = DictType(StringType())