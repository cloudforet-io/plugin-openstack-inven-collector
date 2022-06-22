from spaceone.inventory.conf.settings import get_logger
from spaceone.inventory.manager.resources.metadata.cloud_service import availability_zone as cs_az
from spaceone.inventory.manager.resources.metadata.cloud_service import compute as cs
from spaceone.inventory.manager.resources.metadata.cloud_service import server_group as cs_sg
from spaceone.inventory.manager.resources.metadata.cloud_service_type import availability_zone as cst_az
from spaceone.inventory.manager.resources.metadata.cloud_service_type import compute as cst
from spaceone.inventory.manager.resources.metadata.cloud_service_type import server_group as cst_sg
from spaceone.inventory.manager.resources.resource import BaseResource
from spaceone.inventory.model.resources.block_storage import VolumeModel
from spaceone.inventory.model.resources.compute import ComputeAZModel
from spaceone.inventory.model.resources.compute import ComputeQuotaModel
from spaceone.inventory.model.resources.compute import InstanceModel
from spaceone.inventory.model.resources.compute import NicModel
from spaceone.inventory.model.resources.compute import ServerGroupModel
from spaceone.inventory.model.resources.security_group import SecurityGroupModel

_LOGGER = get_logger(__name__)

PENDING = ['ERROR']
REBOOTING = []
STOPPING = []
RUNNING = ['ACTIVE']
STOPPED = ['STOPPED']
DEALLOCATED = []
TERMINATED = ['SOFT_DELETED', 'DELETED']
STARTING = []
PROVISIONING = ['BUILDING', 'BUILD']
STAGING = ['SHELVED', 'SHELVED_OFFLOADED', 'RESCUED']
SUSPENDING = []
DEALLOCATING = []
SUSPENDED = ['PAUSED', 'SUSPENDED']
REPAIRING = []


class InstanceResource(BaseResource):
    _model_cls = InstanceModel
    _proxy = 'compute'
    _resource = 'servers'
    _cloud_service_type_resource = cst.CLOUD_SERVICE_TYPE
    _cloud_service_meta = cs.CLOUD_SERVICE_METADATA
    _resource_path = "/admin/instances/{id}/detail"
    _native_all_projects_query_support = True
    _native_project_id_query_support = True
    _associated_resource_cls_list = ['VolumeResource', 'SecurityGroupResource', 'HypervisorResource']

    def _set_custom_model_obj_values(self, model_obj: InstanceModel, resource):

        if resource.get('vm_state'):
            self._set_obj_key_value(model_obj, 'vm_state', str(resource.vm_state).upper())

        if resource.get('security_groups'):
            security_group_names = list(dic['name'] for dic in resource.security_groups)
            security_groups = []
            security_group_rules = []

            for security_name in security_group_names:
                security_group = self.get_resource_model_from_associated_resource('SecurityGroupResource',
                                                                                  name=security_name,
                                                                                  project_id=resource.project_id)

                if security_group:
                    security_groups.append(security_group)
                    security_group_rules += security_group.security_group_rules
                else:
                    security_groups.append(SecurityGroupModel({"name": security_name}))

            self._set_obj_key_value(model_obj, 'security_groups', security_groups)
            self._set_obj_key_value(model_obj, 'security_group_rules', security_group_rules)

        if resource.get('attached_volumes'):
            attached_ids = list(dic['id'] for dic in resource.attached_volumes)
            attached_volumes = []
            total_volume_size = 0

            for attached_id in attached_ids:
                volume = self.get_resource_model_from_associated_resource('VolumeResource', id=attached_id)
                if volume:
                    total_volume_size += volume.size_gb
                    attached_volumes.append(volume)
                    if volume.is_bootable and volume.get('volume_image_metadata'):
                        self._set_obj_key_value(model_obj, 'image_id',
                                                volume.get('volume_image_metadata').get('image_id'))
                        self._set_obj_key_value(model_obj, 'image_name',
                                                volume.get('volume_image_metadata').get('image_name'))
                else:
                    attached_volumes.append(VolumeModel({"id": attached_id}))

            self._set_obj_key_value(model_obj, 'volumes', attached_volumes)
            self._set_obj_key_value(model_obj, 'volume_count', len(attached_volumes))
            self._set_obj_key_value(model_obj, 'total_volume_size', total_volume_size)

        if resource.get('addresses'):
            address_list = []
            addresses = resource.addresses
            for network_name, network_values in addresses.items():

                for network_value in network_values:
                    nic_dic = {'network_name': network_name, 'mac_addr': network_value.get("OS-EXT-IPS-MAC:mac_addr"),
                               'type': network_value.get("OS-EXT-IPS:type"), 'addr': network_value.get("addr"),
                               'version': network_value.get("version")}

                    address_list.append(NicModel(nic_dic))

            self._set_obj_key_value(model_obj, 'addresses', address_list)

        if resource.get('flavor'):

            dic = resource.flavor

            if 'original_name' in dic:
                dic['name'] = dic['original_name']

            self._set_obj_key_value(model_obj, 'flavor', dic)

        if resource.get('compute_host'):

            hypervisor_name = resource.compute_host
            hypervisor = self.get_resource_model_from_associated_resource('HypervisorResource',
                                                                          name=hypervisor_name)

            self._set_obj_key_value(model_obj, 'hypervisor_name', hypervisor_name)

            if hypervisor:
                self._set_obj_key_value(model_obj, 'hypervisor_id', hypervisor.id)

        if not self.is_associated_resource:
            self._set_standard_server_schema(model_obj, resource)

        _LOGGER.debug(model_obj.to_primitive())

    def _set_standard_server_schema(self, model_obj: InstanceModel, resource):

        _LOGGER.debug(f"Updating standard server schema")

        if resource.get('addresses'):

            index = 0
            ip_addresses = []
            nics = []
            addresses = resource.addresses
            primary_ip_address = None

            for network_name, network_values in addresses.items():
                for network_value in network_values:

                    ip_address = network_value.get("addr")

                    if network_value.get("addr"):
                        ip_addresses.append(ip_address)

                    nic = {'device_index': index, 'mac_address': network_value.get("OS-EXT-IPS-MAC:mac_addr"),
                           'ip_addresses': [ip_address]}

                    nics.append(nic)

                    if not primary_ip_address:
                        if network_value.get("OS-EXT-IPS:type") == 'fixed' and network_value.get("version") == 4:
                            primary_ip_address = ip_address

                    index += 1

            self._set_obj_key_value(model_obj, 'nics', nics)
            self._set_obj_key_value(model_obj, 'ip_addresses', ip_addresses)

            if primary_ip_address:
                self._set_obj_key_value(model_obj, 'primary_ip_address', primary_ip_address)

        if model_obj.volumes:
            index = 0
            disks = []

            for volume in model_obj.volumes:

                if volume:
                    disk = {'device_index': index, 'disk_type': volume.volume_type, 'size': volume.size_gb}
                    devices = []

                    if volume.attachments:
                        for attachment in volume.attachments:
                            if attachment.get('device'):
                                devices.append(attachment.get('device'))

                        if devices:
                            disk['device'] = ','.join(devices)

                    disks.append(disk)

            self._set_obj_key_value(model_obj, 'disks', disks)

        compute = {'keypair': resource.get('key_name'), 'az': resource.get('availability_zone'),
                   'instance_id': resource.get('id'), 'instance_name': resource.get('name'),
                   'image': model_obj.image_name, 'launched_at': resource.get('created_at')}

        if resource.get('flavor'):
            flavor = resource.flavor
            hardware = {'core': flavor.get("vcpus")}

            if flavor.get("ram"):
                hardware['memory'] = round(flavor.get("ram") / 1024, 3)

            instance_type = flavor.get("name")

            self._set_obj_key_value(model_obj, 'hardware', hardware)

            if flavor.get("vcpus"):
                self._set_obj_key_value(model_obj, 'size', int(flavor.get("vcpus")))

            compute['instance_type'] = instance_type

        if resource.get('vm_state'):
            vm_state = str(resource.vm_state).upper()

            if vm_state in PENDING:
                compute['instance_state'] = 'Pending'
            elif vm_state in REBOOTING:
                compute['instance_state'] = 'Rebooting'
            elif vm_state in STOPPING:
                compute['instance_state'] = 'Stopping'
            elif vm_state in RUNNING:
                compute['instance_state'] = 'Running'
            elif vm_state in STOPPED:
                compute['instance_state'] = 'Stopped'
            elif vm_state in DEALLOCATED:
                compute['instance_state'] = 'Deallocated'
            elif vm_state in TERMINATED:
                compute['instance_state'] = 'Terminated'
            elif vm_state in STARTING:
                compute['instance_state'] = 'Starting'
            elif vm_state in PROVISIONING:
                compute['instance_state'] = 'Provisioning'
            elif vm_state in STAGING:
                compute['instance_state'] = 'Staging'
            elif vm_state in SUSPENDING:
                compute['instance_state'] = 'Suspending'
            elif vm_state in DEALLOCATING:
                compute['instance_state'] = 'Deallocating'
            elif vm_state in SUSPENDED:
                compute['instance_state'] = 'Suspended'
            elif vm_state in REPAIRING:
                compute['instance_state'] = 'Repairing'

        if resource.get('security_groups'):
            security_groups = list(dic['name'] for dic in resource.security_groups)
            compute['security_groups'] = security_groups

        self._set_obj_key_value(model_obj, 'compute', compute)

        if model_obj.security_group_rules:
            security_group = []
            security_group_rules = model_obj.security_group_rules
            for security_group_rule in security_group_rules:
                dic = {
                    "protocol": security_group_rule.protocol,
                    "remote_cidr": security_group_rule.remote_ip_prefix,
                    "security_group_name": security_group_rule.security_group_name,
                    "security_group_id": security_group_rule.security_group_id,
                    "port_range_min": security_group_rule.port_range_min,
                    "port_range_max": security_group_rule.port_range_max,
                }

                if security_group_rule.direction == 'ingress':
                    dic['direction'] = 'inbound'

                elif security_group_rule.direction == 'egress':
                    dic['direction'] = 'outbound'

                # openstack SG support allow only
                dic['action'] = 'allow'

                security_group.append(dic)

            self._set_obj_key_value(model_obj, 'security_group', security_group)


class ComputeQuotaResource(BaseResource):
    _model_cls = ComputeQuotaModel
    _proxy = 'compute'
    _resource = 'get_quota_set_detail'
    _resource_path = "/identity/"
    _native_all_projects_query_support = False
    _native_project_id_query_support = True
    _project_key = 'project'


class ComputeAZResource(BaseResource):
    _model_cls = ComputeAZModel
    _proxy = 'compute'
    _resource = 'availability_zones'
    _resource_path = "/admin/aggregates/"
    _native_all_projects_query_support = False
    _native_project_id_query_support = False
    _cloud_service_type_resource = cst_az.CLOUD_SERVICE_TYPE
    _cloud_service_meta = cs_az.CLOUD_SERVICE_METADATA
    _associated_resource_cls_list = ['HypervisorResource']

    def __init__(self, conn, *args, **kwargs):
        super().__init__(conn, True, **kwargs)  # details=True

    def _set_custom_model_obj_values(self, model_obj: ComputeAZModel, resource):

        # AZ does not have ID. So project id used for creating unique id
        location_project_id = self.get_location_project_id(resource)

        if location_project_id:
            self._set_obj_key_value(model_obj, 'id',
                                    f"{location_project_id}-{self.resource_name.lower()}-{resource.name.lower()}")

        if resource.get('hosts'):
            hosts = resource.hosts

            if hosts:

                hypervisors = self.get_resource_model_from_associated_resources('HypervisorResource')
                hosts_list = []

                total_running_vms = 0

                total_memory_size = 0
                total_memory_used = 0
                total_memory_free = 0

                total_vcpus = 0
                total_vcpus_used = 0
                total_vcpus_free = 0

                for hypervisor in hypervisors:
                    if hypervisor.name in hosts.keys():
                        hosts_list.append(hypervisor)

                        if hypervisor.running_vms:
                            total_running_vms += hypervisor.running_vms
                        if hypervisor.memory_size:
                            total_memory_size += hypervisor.memory_size
                        if hypervisor.memory_used:
                            total_memory_used += hypervisor.memory_used
                        if hypervisor.memory_free:
                            total_memory_free += hypervisor.memory_free
                        if hypervisor.vcpus:
                            total_vcpus += hypervisor.vcpus
                        if hypervisor.vcpus_used:
                            total_vcpus_used += hypervisor.vcpus_used
                        if hypervisor.vcpus_free:
                            total_vcpus_free += hypervisor.vcpus_free

                self._set_obj_key_value(model_obj, 'hypervisors', hosts_list)

                self._set_obj_key_value(model_obj, 'total_running_vms', total_running_vms)

                self._set_obj_key_value(model_obj, 'total_memory_size', total_memory_size)
                self._set_obj_key_value(model_obj, 'total_memory_used', total_memory_used)
                self._set_obj_key_value(model_obj, 'total_memory_free', total_memory_free)

                self._set_obj_key_value(model_obj, 'total_vcpus', total_vcpus)
                self._set_obj_key_value(model_obj, 'total_vcpus_used', total_vcpus_used)
                self._set_obj_key_value(model_obj, 'total_vcpus_free', total_vcpus_free)


class ServerGroupResource(BaseResource):
    _model_cls = ServerGroupModel
    _proxy = 'compute'
    _resource = 'server_groups'
    _is_admin_dashboard = False
    _resource_path = "/ngdetails/OS::Nova::ServerGroup/{id}"
    _native_all_projects_query_support = True
    _native_project_id_query_support = True
    _cloud_service_type_resource = cst_sg.CLOUD_SERVICE_TYPE
    _cloud_service_meta = cs_sg.CLOUD_SERVICE_METADATA
    _associated_resource_cls_list = ['InstanceResource']

    def _set_custom_model_obj_values(self, model_obj: ServerGroupModel, resource):

        if resource.get('member_ids'):
            instances = []
            member_ids = resource.get('member_ids')

            if member_ids:
                self._set_obj_key_value(model_obj, 'member_count', len(member_ids))

            for member_id in member_ids:
                if member_id:
                    instance = self.get_resource_model_from_associated_resource('InstanceResource',
                                                                                id=member_id)
                    instances.append(instance)

            self._set_obj_key_value(model_obj, 'instances', instances)
