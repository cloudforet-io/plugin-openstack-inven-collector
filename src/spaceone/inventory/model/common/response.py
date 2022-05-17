from schematics import Model
from schematics.types import ListType, StringType, PolyModelType, DictType, ModelType

from spaceone.inventory.model.common.base import CloudServiceResource
from spaceone.inventory.model.common.base import CloudServiceTypeResource
from spaceone.inventory.model.common.base import ErrorResource
from spaceone.inventory.model.common.region import RegionModel


class BaseResponse(Model):
    state = StringType(default='SUCCESS', choices=('SUCCESS', 'FAILURE', 'TIMEOUT'))
    message = StringType(default='')
    resource_type = StringType(required=True)
    match_rules = DictType(ListType(StringType), serialize_when_none=False)
    resource = PolyModelType(Model, default={})


class RegionResponse(BaseResponse):
    resource_type = StringType(default='inventory.Region')
    match_rules = DictType(ListType(StringType), default={'1': ['provider', 'region_code']})
    resource = PolyModelType(RegionModel)


class CloudServiceTypeResponse(BaseResponse):
    resource_type = StringType(default='inventory.CloudServiceType')
    match_rules = DictType(ListType(StringType), default={'1': ['name', 'group', 'provider']})
    resource = PolyModelType(CloudServiceTypeResource)


class CloudServiceTypeResourceResponse(BaseResponse):
    state = StringType(default='SUCCESS')
    resource_type = StringType(default='inventory.CloudServiceType')
    match_rules = DictType(ListType(StringType), default={'1': ['name', 'group', 'provider']})
    resource = PolyModelType(CloudServiceTypeResource)


class CloudServiceResponse(BaseResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['reference.resource_id', 'provider', 'cloud_service_type', 'cloud_service_group', 'account']
    })
    resource_type = StringType(default='inventory.CloudService')
    resource = PolyModelType(CloudServiceResource)


class ErrorResourceResponse(CloudServiceResponse):
    state = StringType(default='FAILURE')
    resource_type = StringType(default='inventory.ErrorResource')
    resource = ModelType(ErrorResource, default={})
