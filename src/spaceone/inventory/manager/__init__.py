from spaceone.inventory.manager.openstack_manager import OpenstackManager
from spaceone.inventory.manager.region_manager import RegionManager

__all__ = [
    'RegionManager',
    'OpenstackManager'
]


def list_manager():
    return __all__
