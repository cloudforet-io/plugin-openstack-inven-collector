import logging
from openstack.compute.v2.hypervisor import Hypervisor

from spaceone.inventory.manager.resources.metadata.cloud_service import hypervisor as cs
from spaceone.inventory.manager.resources.metadata.cloud_service_type import hypervisor as cst
from spaceone.inventory.manager.resources.resource import BaseResource
from spaceone.inventory.model.resources.hypervisor import HypervisorModel

_LOGGER = logging.getLogger(__name__)


class HypervisorResource(BaseResource):
    _model_cls = HypervisorModel
    _proxy = 'compute'
    _resource = 'hypervisors'
    _resource_path = "/admin/hypervisors"
    _cloud_service_type_resource = cst.CLOUD_SERVICE_TYPE
    _cloud_service_meta = cs.CLOUD_SERVICE_METADATA
    _native_all_projects_query_support = False
    _native_project_id_query_support = False
    _associated_resource_cls_list = ['InstanceResource']

    def __init__(self, conn, **kwargs):
        super().__init__(conn, **kwargs)
        self._default_args = (True,)  # details=True

    def _collect_associated_resource(self, **kwargs):
        super()._collect_associated_resource(all_projects=True)

    def _set_custom_model_obj_values(self, model_obj: HypervisorModel, resource: Hypervisor):

        if resource.get('memory_size') and resource.memory_size != 0:
            self._set_obj_key_value(model_obj, 'memory_size', int(resource.memory_size / 1024))

        if resource.get('memory_used') and resource.memory_used != 0:
            self._set_obj_key_value(model_obj, 'memory_used', int(resource.memory_used / 1024))

        if resource.get('memory_free') and resource.memory_free != 0:
            self._set_obj_key_value(model_obj, 'memory_free', abs(int(resource.memory_free / 1024)))

        if resource.get('name'):
            instances = self.get_resource_model_from_associated_resources('servers', compute_host=resource.name)
            self._set_obj_key_value(model_obj, 'instances', instances)
