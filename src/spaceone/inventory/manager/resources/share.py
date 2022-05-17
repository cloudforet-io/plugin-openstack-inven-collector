import logging
from openstack.shared_file_system.v2.share import Share

from spaceone.inventory.manager.resources.metadata.cloud_service import share as cs
from spaceone.inventory.manager.resources.metadata.cloud_service_type import share as cst
from spaceone.inventory.manager.resources.resource import BaseResource
from spaceone.inventory.model.resources.share import ShareModel

_LOGGER = logging.getLogger(__name__)

class ShareResource(BaseResource):
    _model_cls = ShareModel
    _proxy = 'share'
    _resource = 'shares'
    _cloud_service_type_resource = cst.CLOUD_SERVICE_TYPE
    _cloud_service_meta = cs.CLOUD_SERVICE_METADATA
    _resource_path = "/auth/switch/{project_id}/?next=/project/shares/{id}"
    _native_all_projects_query_support = True
    _native_project_id_query_support = True

    def __init__(self, conn, **kwargs):
        super().__init__(conn, **kwargs)
        self._default_args = (True,)  # details=True

    def _set_custom_model_obj_values(self, model_obj: ShareModel, resource: Share):

        if resource.get('size'):
            giga_to_byte = 1024 * 1024 * 1024
            self._set_obj_key_value(model_obj, 'size_gb', resource.size)
            self._set_obj_key_value(model_obj, 'size', resource.size * giga_to_byte)
