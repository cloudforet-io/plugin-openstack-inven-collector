from spaceone.inventory.conf.global_conf import get_logger
from openstack.block_storage.v2.volume import Volume

from spaceone.inventory.manager.resources.metadata.cloud_service import block_storage as cs
from spaceone.inventory.manager.resources.metadata.cloud_service_type import block_storage as cst
from spaceone.inventory.manager.resources.resource import BaseResource
from spaceone.inventory.model.resources.block_storage import VolumeModel
from spaceone.inventory.model.resources.block_storage import VolumeQuotaModel
from spaceone.inventory.error.base import CollectorError

from typing import (
    List,
    Dict,
    Any
)

_LOGGER = get_logger(__name__)


class VolumeResource(BaseResource):
    _model_cls = VolumeModel
    _proxy = 'block_storage'
    _resource = 'volumes'
    _cloud_service_type_resource = cst.CLOUD_SERVICE_TYPE
    _cloud_service_meta = cs.CLOUD_SERVICE_METADATA
    _resource_path = "/auth/switch/{project_id}/?next=/project/volumes/{id}"
    _native_all_projects_query_support = True
    _native_project_id_query_support = True

    def _set_custom_model_obj_values(self, model_obj: VolumeModel, resource: Volume):

        if resource.get('attachments') and isinstance(resource.attachments, list) and len(resource.attachments) > 1:
            self._set_obj_key_value(model_obj, 'multiattach', True)

        if resource.get('size'):
            giga_to_byte = 1024 * 1024 * 1024
            self._set_obj_key_value(model_obj, 'size_gb', resource.size)
            self._set_obj_key_value(model_obj, 'size', resource.size * giga_to_byte)


class VolumeQuotaResource(BaseResource):
    _model_cls = VolumeQuotaModel
    _proxy = 'block_storage'
    _resource = 'get_quota_set'
    _resource_path = "/project/"
    _native_all_projects_query_support = False
    _native_project_id_query_support = True
    _project_key = 'project'

    def __init__(self, conn, **kwargs):
        super().__init__(conn, **kwargs)
        self._default_kwargs = {"usage": True}
