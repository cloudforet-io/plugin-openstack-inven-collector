from schematics import Model
from spaceone.inventory.model.common.region import RegionModel
from spaceone.inventory.model import ResourceModel
from schematics.types import ListType, StringType, PolyModelType, DictType, ModelType, FloatType

class BaseResponse(Model):
    state = StringType(default='SUCCESS', choices=('SUCCESS', 'FAILURE', 'TIMEOUT'))
    message = StringType(default='')
    resource_type = StringType(required=True)
    match_rules = DictType(ListType(StringType), serialize_when_none=False)
    resource = PolyModelType(Model, default={})


class CloudServiceResponse(BaseResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['reference.self_link', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource_type = StringType(default='inventory.CloudService')
    resources = ListType(ModelType(ResourceModel), serialize_when_none=False)


class ErrorResource(Model):
    resource_type = StringType(default='inventory.CloudService')
    provider = StringType(default="openstack")
    cloud_service_group = StringType(default='ComputeEngine', serialize_when_none=False)
    cloud_service_type = StringType(default='Instance', serialize_when_none=False)
    resource_id = StringType(serialize_when_none=False)


class ErrorResourceResponse(CloudServiceResponse):
    state = StringType(default='FAILURE')
    resource_type = StringType(default='inventory.ErrorResource')
    resource = ModelType(ErrorResource, default={})


class RegionResponse(BaseResponse):
    resource_type = StringType(default='inventory.Region')
    match_rules = DictType(ListType(StringType), default={'1': ['provider', 'region_code']})
    resource = PolyModelType(RegionModel)

