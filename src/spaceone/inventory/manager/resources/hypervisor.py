from spaceone.inventory.conf.global_conf import get_logger

from openstack.compute.v2.hypervisor import Hypervisor

from spaceone.inventory.manager.resources.metadata.cloud_service import hypervisor as cs
from spaceone.inventory.manager.resources.metadata.cloud_service_type import hypervisor as cst
from spaceone.inventory.manager.resources.resource import BaseResource
from spaceone.inventory.model.resources.hypervisor import HypervisorModel

_LOGGER = get_logger(__name__)


class HypervisorResource(BaseResource):
    _model_cls = HypervisorModel
    _proxy = 'compute'
    _resource = 'hypervisors'
    _resource_path = "/admin/hypervisors"
    _cloud_service_type_resource = cst.CLOUD_SERVICE_TYPE
    _cloud_service_meta = cs.CLOUD_SERVICE_METADATA
    _native_all_projects_query_support = False
    _native_project_id_query_support = False
    _associated_resource_cls_list = ['InstanceResource', 'ComputeAZResource']

    def __init__(self, conn, **kwargs):
        super().__init__(conn, **kwargs)
        self._default_args = (True,)  # details=True

    def _collect_associated_resource(self, **kwargs):
        super()._collect_associated_resource(all_projects=True, default_project_id=self.default_project_id)

    def _set_custom_model_obj_values(self, model_obj: HypervisorModel, resource: Hypervisor):

        if resource.get('memory_size'):
            self._set_obj_key_value(model_obj, 'memory_size', resource.memory_size)

        if resource.get('memory_used'):
            self._set_obj_key_value(model_obj, 'memory_used', resource.memory_used)

        if resource.get('memory_free'):
            self._set_obj_key_value(model_obj, 'memory_free', resource.memory_free)

        if resource.get('name'):
            instances = self.get_resource_model_from_associated_resources('InstanceResource', hypervisor_name=resource.name)
            self._set_obj_key_value(model_obj, 'instances', instances)

            compute_azs = self.get_resource_model_from_associated_resources('ComputeAZResource')

            for compute_az in compute_azs:
                if compute_az.hosts and compute_az.hosts.get(resource.name):
                    self._set_obj_key_value(model_obj, 'availability_zone', compute_az.name)

        if resource.get('state'):
            self._set_obj_key_value(model_obj, 'state', str(resource.state).upper())

        if resource.get('status'):
            self._set_obj_key_value(model_obj, 'status', str(resource.status).upper())
