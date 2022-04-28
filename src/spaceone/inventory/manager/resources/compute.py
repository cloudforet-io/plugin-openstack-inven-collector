from spaceone.inventory.model.resources.compute import InstanceModel
from spaceone.inventory.model.resources.compute import FlavorModel
from spaceone.inventory.model.resources.block_storage import VolumeModel
from spaceone.inventory.manager.resources.resource import BaseResource
from spaceone.inventory.manager.resources.metadata.cloud_service_type import compute as cst_compute
from spaceone.inventory.manager.resources.metadata.cloud_service import compute as cs_compute
from openstack.compute.v2.server import Server

from typing import (
    List,
    Dict
)


class InstanceResource(BaseResource):
    _model_cls = InstanceModel
    _proxy = 'compute'
    _resource = 'servers'
    _cloud_service_type_resource = cst_compute.CLOUD_SERVICE_TYPE
    _cloud_service_meta = cs_compute.CLOUD_SERVICE_METADATA
    _project_resource = "/project/instances/"

    @property
    def resources(self) -> List[Server]:
        return super().resources

    def _set_default_model_obj_values(self, model_obj: InstanceModel, resource: Server):

        ## insert custom data
        if hasattr(resource, 'location') and hasattr(resource.location, 'region_name'):
            self._set_obj_key_value(model_obj, 'region_name', resource.location.region_name)

        if hasattr(resource, 'security_groups') and getattr(resource, 'security_groups') is not None:
            security_groups = list(dic['name'] for dic in resource.security_groups)
            self._set_obj_key_value(model_obj, 'security_groups', security_groups)

        if hasattr(resource, 'attached_volumes') and getattr(resource, 'attached_volumes') is not None:
            attached_ids = list(dic['id'] for dic in resource.attached_volumes)
            attached_volumes = []

            for attached_id in attached_ids:
                attached_volumes.append(VolumeModel({"id": attached_id}))

            self._set_obj_key_value(model_obj, 'volumes', attached_volumes)

        if hasattr(resource, 'addresses'):
            minimal_addresses = []
            addresses = resource.addresses
            for network_name, network_values in addresses.items():
                for network_value in network_values:
                    if 'addr' in network_value:
                        minimal_addresses.append(network_value.get("addr"))

            self._set_obj_key_value(model_obj, 'minimal_addresses', minimal_addresses)

        if hasattr(resource, 'flavor'):

            dic = resource.flavor

            if 'original_name' in dic:
                dic['name'] = dic['original_name']
                del dic['original_name']

            self._set_obj_key_value(model_obj, 'flavor', FlavorModel(dic))


class FlavorResource(BaseResource):
    _model_cls = FlavorModel
    _proxy = 'compute'
    _resource = 'flavors'
    _cloud_service_type = 'Flavor'
    _cloud_service_group = 'Compute'
