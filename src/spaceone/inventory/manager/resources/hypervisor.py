from spaceone.inventory.conf.settings import get_logger
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

    def __init__(self, conn, *args, **kwargs):
        super().__init__(conn, True, with_servers=True)

    def _collect_associated_resource(self, *args, **kwargs):

        for class_name in self._associated_resource_cls_list:

            if class_name == 'InstanceResource':
                associated_resource = self.get_resource_class(class_name)(self._conn, all_projects=True)
            elif class_name == 'ComputeAZResource':
                associated_resource = self.get_resource_class(class_name)(self._conn, )

            if associated_resource:
                _LOGGER.info(f"Collecting related resources : {associated_resource.resource_name}")

            try:
                for resource in associated_resource.collect():
                    self._associated_resource_list.append(resource)
            except Exception as e:
                _LOGGER.error(e)
                raise

    def _get_free_space(self, ratio, total, used):
        return (ratio * total) - used

    def __get_placement_info(self, hypervisor_id: str):

        inventories = self._conn.placement.get_resource_providers_inventories(hypervisor_id).get('inventories')
        usages = self._conn.placement.get_resource_providers_usages(hypervisor_id).get('usages')

        if inventories and usages:
            dic = {
                "local_disk_size": inventories.get('DISK_GB').get('total'),
                "local_disk_used": usages.get('DISK_GB'),
                "local_disk_allocation_ratio": inventories.get('DISK_GB').get('allocation_ratio'),
                "memory_size": inventories.get('MEMORY_MB').get('total'),
                "memory_used": usages.get('MEMORY_MB'),
                "memory_allocation_ratio": inventories.get('MEMORY_MB').get('allocation_ratio'),
                "vcpus": inventories.get('VCPU').get('total'),
                "vcpus_used": usages.get('VCPU'),
                "vcpus_allocation_ratio": inventories.get('VCPU').get('allocation_ratio'),
            }

            dic["local_disk_free"] = self._get_free_space(dic['local_disk_allocation_ratio'], dic['local_disk_size'],
                                                          dic['local_disk_used'])
            dic["memory_free"] = self._get_free_space(dic['memory_allocation_ratio'], dic['memory_size'],
                                                      dic['memory_used'])
            dic["vcpus_free"] = self._get_free_space(dic['vcpus_allocation_ratio'], dic['vcpus'], dic['vcpus_used'])

            return dic

        return None

    def _set_custom_model_obj_values(self, model_obj: HypervisorModel, resource):

        placement_info = None

        try:
            placement_info = self.__get_placement_info(resource.id)
        except Exception as e:
            _LOGGER.warn(f"Getting placement info failed : {e}")

        if placement_info:
            self._set_obj_key_value(model_obj, 'vcpus_free', placement_info['vcpus_free'])
            self._set_obj_key_value(model_obj, 'vcpus_used', placement_info['vcpus_used'])
            self._set_obj_key_value(model_obj, 'vcpus', placement_info['vcpus'])
            self._set_obj_key_value(model_obj, 'memory_size', placement_info['memory_size'])
            self._set_obj_key_value(model_obj, 'memory_used', placement_info['memory_used'])
            self._set_obj_key_value(model_obj, 'memory_free', placement_info['memory_free'])
            self._set_obj_key_value(model_obj, 'local_disk_size', placement_info['local_disk_size'])
            self._set_obj_key_value(model_obj, 'local_disk_used', placement_info['local_disk_used'])
            self._set_obj_key_value(model_obj, 'local_disk_free', placement_info['local_disk_free'])
            self._set_obj_key_value(model_obj, 'local_disk_allocation_ratio',
                                    placement_info['local_disk_allocation_ratio'])
            self._set_obj_key_value(model_obj, 'vcpus_allocation_ratio', placement_info['vcpus_allocation_ratio'])
            self._set_obj_key_value(model_obj, 'memory_allocation_ratio', placement_info['memory_allocation_ratio'])

        else:
            self._set_obj_key_value(model_obj, 'vcpus', resource.vcpus)
            self._set_obj_key_value(model_obj, 'vcpus_free', resource.vcpus_free)
            self._set_obj_key_value(model_obj, 'vcpus_used', resource.vcpus_used)
            self._set_obj_key_value(model_obj, 'memory_size', resource.memory_size)
            self._set_obj_key_value(model_obj, 'memory_used', resource.memory_used)
            self._set_obj_key_value(model_obj, 'memory_free', resource.memory_free)
            self._set_obj_key_value(model_obj, 'local_disk_size', resource.local_disk_size)
            self._set_obj_key_value(model_obj, 'local_disk_free', resource.local_disk_free)
            self._set_obj_key_value(model_obj, 'local_disk_used', resource.local_disk_used)

        if resource.get('servers'):
            instances = []
            servers = resource.get('servers')

            if servers:
                for server in servers:
                    instance = self.get_resource_model_from_associated_resource('InstanceResource',
                                                                                id=server.get("uuid"))
                    instances.append(instance)

                self._set_obj_key_value(model_obj, 'instances', instances)
                self._set_obj_key_value(model_obj, 'running_vms', len(resource.servers))

        compute_azs = self.get_resource_model_from_associated_resources('ComputeAZResource')

        if compute_azs:
            for compute_az in compute_azs:
                if compute_az.hosts and compute_az.hosts.get(resource.name):
                    self._set_obj_key_value(model_obj, 'availability_zone', compute_az.name)

        if resource.get('state'):
            self._set_obj_key_value(model_obj, 'state', str(resource.state).upper())

        if resource.get('status'):
            self._set_obj_key_value(model_obj, 'status', str(resource.status).upper())
