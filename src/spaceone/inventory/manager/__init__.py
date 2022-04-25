from spaceone.inventory.manager.region_manager import RegionManager
from spaceone.inventory.manager.openstack_manager import OpenstackManager

__all__ = [
    'RegionManager',
    'OpenstackManager'
]

def list_manager():
    return __all__
