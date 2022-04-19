from spaceone.inventory.model.network.data import NetworkModel
from spaceone.inventory.manager.resources.resource import BaseResource
from openstack.network.v2.network import Network
from typing import (
    Any,
    Iterable,
    List,
    Dict,
    Optional,
    Type,
    Union,
    Tuple,
    Iterator
)


class NetworkResource(BaseResource):
    _model_cls = NetworkModel
    _proxy = 'network'
    _resource = 'networks'

    @property
    def resources(self) -> List[Network]:
        return super().resources

    def _set_default_model_obj_values(self, model_obj: NetworkModel, resource: Network):
        pass
