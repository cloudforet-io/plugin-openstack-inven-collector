from spaceone.inventory.conf.settings import get_logger
from spaceone.inventory.manager.resources.metadata.cloud_service import image as cs
from spaceone.inventory.manager.resources.metadata.cloud_service_type import image as cst
from spaceone.inventory.manager.resources.resource import BaseResource
from spaceone.inventory.model.resources.image import ImageModel

_LOGGER = get_logger(__name__)


class ImageResource(BaseResource):
    _model_cls = ImageModel
    _proxy = 'image'
    _resource = 'images'
    _is_admin_dashboard = False
    _resource_path = "/ngdetails/OS::Glance::Image/{id}"
    _cloud_service_type_resource = cst.CLOUD_SERVICE_TYPE
    _cloud_service_meta = cs.CLOUD_SERVICE_METADATA

    def _set_custom_model_obj_values(self, model_obj: ImageModel, resource):

        if resource.get('status'):
            self._set_obj_key_value(model_obj, 'status', str(resource.status).upper())

        if resource.get('owner_id') and self._projects.get(resource.get('owner_id')):
            project_name = self._projects[resource.get('owner_id')].get("name")
            self._set_obj_key_value(model_obj, 'project_name', project_name)
            self._set_obj_key_value(model_obj, 'project_id', resource.get('owner_id'))

        if resource.get('size'):
            byte_to_mega = 1024 * 1024
            self._set_obj_key_value(model_obj, 'size_mb', resource.size / byte_to_mega)
