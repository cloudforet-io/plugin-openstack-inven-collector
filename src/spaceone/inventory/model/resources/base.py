from schematics import Model
from schematics.types import StringType, ModelType, BooleanType, ListType


class ReferenceModel(Model):
    class Option:
        serialize_when_none = False

    bookmark_link = StringType()
    self_link = StringType()

class ResourceModel(Model):
    id = StringType(default=None, serialize_when_none=False)
    reference = ModelType(ReferenceModel, serialize_when_none=False)
    external_link = StringType()
    region_name = StringType()
    project_id = StringType(serialize_when_none=False)
    project_name = StringType(serialize_when_none=False)
    tags = ListType(StringType, default=[])

class Secret(Model):
    username = StringType(required=True)
    password = StringType(required=True)
    project_id = StringType(required=True)
    user_domain_name = StringType(required=True, default="Default")
    region_name = StringType(required=True, default="RegionOne")
    auth_url = StringType(required=True)
    interface = StringType(default="public")
    identity_api_version = StringType(default="3")
    dashboard_url = StringType(default=None)
    all_projects = BooleanType(default=False)


