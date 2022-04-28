from spaceone.inventory.model.resources.network import NetworkModel
from spaceone.inventory.manager.resources.resource import BaseResource
from spaceone.inventory.manager.resources.metadata.cloud_service_type import network as cst_network
from spaceone.inventory.manager.resources.metadata.cloud_service import network as cs_network
from openstack.network.v2.network import Network
from typing import (
    List,
    Dict
)


class NetworkResource(BaseResource):
    _model_cls = NetworkModel
    _proxy = 'network'
    _resource = 'networks'
    _cloud_service_type_resource = cst_network.CLOUD_SERVICE_TYPE
    _cloud_service_meta = cs_network.CLOUD_SERVICE_METADATA
    _project_resource = "/project/networks/"

    @property
    def resources(self) -> List[Network]:
        return super().resources

    def _set_default_model_obj_values(self, model_obj: NetworkModel, resource: Network):
        pass
