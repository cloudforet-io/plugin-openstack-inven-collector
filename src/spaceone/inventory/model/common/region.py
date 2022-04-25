from schematics import Model
from schematics.types import StringType, DictType


class RegionModel(Model):
    region_code = StringType(required=True)
    provider = StringType(default='openstack')
    name = StringType(default='', required=True)
    tags = DictType(StringType, serialize_when_none=False)