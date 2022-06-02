# all openstack resources
OS_RESOURCE_MAP = {
    "InstanceResource": "spaceone.inventory.manager.resources.compute",
    "HypervisorResource": "spaceone.inventory.manager.resources.hypervisor",
    "VolumeResource": "spaceone.inventory.manager.resources.block_storage",
    "NetworkResource": "spaceone.inventory.manager.resources.network",
    "SubnetResource": "spaceone.inventory.manager.resources.network",
    "SecurityGroupResource": "spaceone.inventory.manager.resources.security_group",
    "ShareResource": "spaceone.inventory.manager.resources.share",
    "ShareNetworkResource": "spaceone.inventory.manager.resources.share",
    "ProjectResource": "spaceone.inventory.manager.resources.project",
    "UserResource": "spaceone.inventory.manager.resources.user",
    "RoleResource": "spaceone.inventory.manager.resources.user",
    "RoleAssignmentResource": "spaceone.inventory.manager.resources.user",
    "ComputeQuotaResource": "spaceone.inventory.manager.resources.compute",
    "VolumeQuotaResource": "spaceone.inventory.manager.resources.block_storage",
    "ComputeAZResource": "spaceone.inventory.manager.resources.compute",
    "StorageResource": "spaceone.inventory.manager.resources.storage",
}

# to do not show resources on spaceone view
# Internally used for associated resources
IGNORE_RESOURCE_LIST = ["RoleResource", "RoleAssignmentResource", "ShareNetworkResource", "ComputeQuotaResource",
                        "VolumeQuotaResource"]
