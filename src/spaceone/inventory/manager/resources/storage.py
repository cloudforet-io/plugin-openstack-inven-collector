from typing import (
    List,
    Any,
)

from spaceone.inventory.conf.global_conf import get_logger
from spaceone.inventory.error.base import CollectorError
from spaceone.inventory.manager.resources.metadata.cloud_service import storage as cs
from spaceone.inventory.manager.resources.metadata.cloud_service_type import storage as cst
from spaceone.inventory.manager.resources.resource import BaseResource
from spaceone.inventory.model.resources.storage import StorageModel

_LOGGER = get_logger(__name__)


class StorageResource(BaseResource):
    _model_cls = StorageModel
    _cloud_service_type_resource = cst.CLOUD_SERVICE_TYPE
    _cloud_service_meta = cs.CLOUD_SERVICE_METADATA

    @property
    def resources(self) -> List[Any]:

        if self._conn is None:
            raise CollectorError(message='secret_data must exist')

        dic_volumes = {}
        storage_backend_list = []

        volumes = self._conn.block_storage.volumes(all_projects=True)

        for volume in volumes:

            if volume.host is None:
                continue

            if volume.host not in dic_volumes:
                dic_volumes[volume.host] = {
                    'total_allocated_volume_size': 0,
                    'total_volume_count': 0,
                    'attached_volume_count': 0,
                    'available_volume_count': 0,
                }

            dic_volumes[volume.host]['total_volume_count'] += 1
            dic_volumes[volume.host]['total_allocated_volume_size'] += volume.size

            if volume.status == 'in-use':
                dic_volumes[volume.host]['attached_volume_count'] += 1

            if volume.status == 'available':
                dic_volumes[volume.host]['available_volume_count'] += 1

        for host_name in dic_volumes.keys():
            capabilities = self._conn.block_storage.get_capabilities(host_name)
            capabilities = capabilities.toDict()

            capabilities['total_allocated_volume_size'] = dic_volumes.get(host_name).get('total_allocated_volume_size')
            capabilities['total_volume_count'] = dic_volumes.get(host_name).get('total_volume_count')
            capabilities['attached_volume_count'] = dic_volumes.get(host_name).get('attached_volume_count')
            capabilities['available_volume_count'] = dic_volumes.get(host_name).get('available_volume_count')

            storage_backend_list.append(capabilities)

        return storage_backend_list
