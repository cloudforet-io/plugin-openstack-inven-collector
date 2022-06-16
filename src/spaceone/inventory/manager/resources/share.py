from spaceone.inventory.conf.settings import get_logger
from spaceone.inventory.manager.resources.metadata.cloud_service import share as cs
from spaceone.inventory.manager.resources.metadata.cloud_service_type import share as cst
from spaceone.inventory.manager.resources.resource import BaseResource
from spaceone.inventory.model.common.response import CloudServiceTypeResource
from spaceone.inventory.model.resources.share import ShareModel, ShareNetworkModel

_LOGGER = get_logger(__name__)


class ShareResource(BaseResource):
    _model_cls = ShareModel
    _proxy = 'share'
    _resource = 'shares'
    _cloud_service_type_resource = cst.CLOUD_SERVICE_TYPE
    _cloud_service_meta = cs.CLOUD_SERVICE_METADATA
    _resource_path = "/admin/shares/{id}"
    _native_all_projects_query_support = True
    _native_project_id_query_support = True
    _associated_resource_cls_list = ['ShareNetworkResource']

    def __init__(self, conn, *args, **kwargs):
        super().__init__(conn, True, **kwargs)  # details=True

    def _set_custom_model_obj_values(self, model_obj: ShareModel, resource):

        if resource.get('size'):
            giga_to_byte = 1024 * 1024 * 1024
            self._set_obj_key_value(model_obj, 'size_gb', resource.size)
            self._set_obj_key_value(model_obj, 'size', resource.size * giga_to_byte)

        if resource.get('share_network_id'):
            share_network = self.get_resource_model_from_associated_resource('ShareNetworkResource',
                                                                             id=resource.share_network_id)
            self._set_obj_key_value(model_obj, 'share_network', share_network)


class ShareNetworkResource(BaseResource):
    _model_cls = ShareNetworkModel
    _proxy = 'share'
    _resource = 'share_networks'
    _is_dashboard_auth_switch = False
    _resource_path = "/admin/share_networks/{id}"
    _cloud_service_type_resource = CloudServiceTypeResource({"name": "ShareNetwork", "group": "Network"})
    _native_all_projects_query_support = True
    _native_project_id_query_support = True

    def __init__(self, conn, **kwargs):
        super().__init__(conn, **kwargs)
        self._default_args = (True,)  # details=True
