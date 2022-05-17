import logging
from openstack.network.v2.network import Network

from spaceone.inventory.manager.resources.metadata.cloud_service import network as cs
from spaceone.inventory.manager.resources.metadata.cloud_service_type import network as cst
from spaceone.inventory.manager.resources.resource import BaseResource
from spaceone.inventory.model.resources.network import NetworkModel
from spaceone.inventory.model.resources.network import SegmentModel
from spaceone.inventory.model.resources.network import SubnetModel

_LOGGER = logging.getLogger(__name__)

class SubnetResource(BaseResource):
    _model_cls = SubnetModel
    _proxy = 'network'
    _resource = 'subnets'
    _resource_path = "/project/networks/subnets/"
    _native_all_projects_query_support = False
    _native_project_id_query_support = True


class NetworkResource(BaseResource):
    _model_cls = NetworkModel
    _proxy = 'network'
    _resource = 'networks'
    _cloud_service_type_resource = cst.CLOUD_SERVICE_TYPE
    _cloud_service_meta = cs.CLOUD_SERVICE_METADATA
    _resource_path = "/auth/switch/{project_id}/?next=/project/networks/{id}/detail"
    _native_all_projects_query_support = False
    _native_project_id_query_support = True
    _associated_resource_cls_list = ['SubnetResource']

    def _set_custom_model_obj_values(self, model_obj: NetworkModel, resource: Network):

        if resource.get('subnet_ids'):
            subnet_ids = resource.subnet_ids
            subnets = []
            minimal_subnets = []
            cidrs = []

            for subnet_id in subnet_ids:
                subnet = self.get_resource_model_from_associated_resource('subnets', id=subnet_id,
                                                                          project_id=resource.project_id)
                if subnet:
                    subnets.append(subnet)
                    minimal_subnets.append(f"{subnet.name} : {subnet.cidr} -> GW {subnet.gateway_ip}")
                    cidrs.append(subnet.cidr)
                else:
                    subnets.append(SubnetModel({"id": subnet_id}))

            self._set_obj_key_value(model_obj, 'minimal_subnets', minimal_subnets)
            self._set_obj_key_value(model_obj, 'subnets', subnets)
            self._set_obj_key_value(model_obj, 'cidrs', cidrs)


class SegmentResource(BaseResource):
    _model_cls = SegmentModel
    _proxy = 'network'
    _resource = 'segments'
