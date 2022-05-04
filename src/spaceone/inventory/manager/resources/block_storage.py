from spaceone.inventory.model.resources.block_storage import VolumeModel
from spaceone.inventory.manager.resources.resource import BaseResource
from spaceone.inventory.model.resources.base import ReferenceModel
from spaceone.inventory.manager.resources.metadata.cloud_service_type import block_storage as cst_blockstorage
from spaceone.inventory.manager.resources.metadata.cloud_service import block_storage as cs_blockstorage
from openstack.block_storage.v2.volume import Volume

from typing import (
    List,
    Dict
)


class VolumeResource(BaseResource):
    _model_cls = VolumeModel
    _proxy = 'block_storage'
    _resource = 'volumes'
    _cloud_service_type_resource = cst_blockstorage.CLOUD_SERVICE_TYPE
    _cloud_service_meta = cs_blockstorage.CLOUD_SERVICE_METADATA
    _resource_path = "/project/volumes/{id}"
    __giga_to_byte = 1024 * 1024 * 1024

    @property
    def resources(self) -> List[Volume]:
        return super().resources

    def _set_default_model_obj_values(self, model_obj: VolumeModel, resource: Volume):

        if hasattr(resource, 'attachments') and len(resource.attachments) > 1:
            self._set_obj_key_value(model_obj, 'multiattach', True)

        if hasattr(resource, 'size'):

            self._set_obj_key_value(model_obj, 'size_gb', resource.size)
            self._set_obj_key_value(model_obj, 'size', resource.size * self.__giga_to_byte)
