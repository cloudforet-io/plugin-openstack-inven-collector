from spaceone.inventory.conf.settings import get_logger
from spaceone.inventory.manager.resources.metadata.cloud_service import block_storage as cs
from spaceone.inventory.manager.resources.metadata.cloud_service import snapshot as cs_snapshot
from spaceone.inventory.manager.resources.metadata.cloud_service_type import block_storage as cst
from spaceone.inventory.manager.resources.metadata.cloud_service_type import snapshot as cst_snapshot
from spaceone.inventory.manager.resources.resource import BaseResource
from spaceone.inventory.model.resources.block_storage import SnapshotModel
from spaceone.inventory.model.resources.block_storage import VolumeModel
from spaceone.inventory.model.resources.block_storage import VolumeQuotaModel

_LOGGER = get_logger(__name__)


class VolumeResource(BaseResource):
    _model_cls = VolumeModel
    _proxy = 'block_storage'
    _resource = 'volumes'
    _cloud_service_type_resource = cst.CLOUD_SERVICE_TYPE
    _cloud_service_meta = cs.CLOUD_SERVICE_METADATA
    _resource_path = "/admin/volumes/{id}"
    _native_all_projects_query_support = True
    _native_project_id_query_support = True

    def _set_custom_model_obj_values(self, model_obj: VolumeModel, resource):

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
    _resource_path = "/identity"
    _native_all_projects_query_support = False
    _native_project_id_query_support = True
    _project_key = 'project'

    def __init__(self, conn, **kwargs):
        super().__init__(conn, **kwargs)
        self._default_kwargs = {"usage": True}


class SnapshotResource(BaseResource):
    _model_cls = SnapshotModel
    _proxy = 'block_storage'
    _resource = 'snapshots'
    _resource_path = "/admin/snapshots/{id}"
    _cloud_service_type_resource = cst_snapshot.CLOUD_SERVICE_TYPE
    _cloud_service_meta = cs_snapshot.CLOUD_SERVICE_METADATA
    _native_all_projects_query_support = True
    _native_project_id_query_support = True

    def __init__(self, conn, *args, **kwargs):
        super().__init__(conn, True, **kwargs)

    def _set_custom_model_obj_values(self, model_obj: VolumeModel, resource):
        if resource.get('size'):
            giga_to_byte = 1024 * 1024 * 1024
            self._set_obj_key_value(model_obj, 'size_gb', resource.size)
            self._set_obj_key_value(model_obj, 'size', resource.size * giga_to_byte)
