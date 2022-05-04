from spaceone.inventory.model.resources.network import NetworkModel
from spaceone.inventory.model.resources.network import SubnetModel
from spaceone.inventory.model.resources.network import SegmentModel
from spaceone.inventory.manager.resources.resource import BaseResource
from spaceone.inventory.model.resources.base import ReferenceModel
from spaceone.inventory.manager.resources.metadata.cloud_service_type import network as cst_network
from spaceone.inventory.manager.resources.metadata.cloud_service import network as cs_network
from openstack.network.v2.network import Network
from openstack.network.v2.subnet import Subnet
from openstack.network.v2.segment import Segment
from urllib.parse import urljoin

from typing import (
    List,
    Dict
)


class SubnetResource(BaseResource):
    _model_cls = SubnetModel
    _proxy = 'network'
    _resource = 'subnets'
    _resource_path = "/project/networks/subnets/"

class NetworkResource(BaseResource):
    _model_cls = NetworkModel
    _proxy = 'network'
    _resource = 'networks'
    _cloud_service_type_resource = cst_network.CLOUD_SERVICE_TYPE
    _cloud_service_meta = cs_network.CLOUD_SERVICE_METADATA
    _resource_path = "/project/networks/{id}/detail"
    _associated_resource_cls_list = [SubnetResource]

    @property
    def resources(self) -> List[Network]:
        return super().resources

    def _set_default_model_obj_values(self, model_obj: NetworkModel, resource: Network):

        if hasattr(resource, 'subnet_ids') and getattr(resource, 'subnet_ids') is not None:
            subnet_ids = resource.subnet_ids
            subnets = []
            minimal_subnets = []

            for subnet_id in subnet_ids:
                subnet = self.get_resource_model_from_associated_resources('subnets', subnet_id)
                if subnet:
                    subnets.append(subnet)
                    minimal_subnets.append(f"{subnet.name} : {subnet.cidr} -> GW {subnet.gateway_ip}")
                else:
                    subnets.append(SubnetModel({"id": subnet_id}))

            self._set_obj_key_value(model_obj, 'minimal_subnets', minimal_subnets)
            self._set_obj_key_value(model_obj, 'subnets', subnets)

class SegmentResource(BaseResource):
    _model_cls = SegmentModel
    _proxy = 'network'
    _resource = 'segments'

    @property
    def resources(self) -> List[Subnet]:
        return super().resources

    def _set_default_model_obj_values(self, model_obj: SegmentModel, resource: Segment):
        pass
