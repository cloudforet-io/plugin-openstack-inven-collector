from typing import (
    Any
)

from spaceone.inventory.manager.resources.metadata.cloud_service import user as cs
from spaceone.inventory.manager.resources.metadata.cloud_service_type import user as cst
from spaceone.inventory.manager.resources.resource import BaseResource
from spaceone.inventory.model.common.response import CloudServiceTypeResource
from spaceone.inventory.model.resources.user import UserModel, RoleModel, RoleAssignmentModel


class UserResource(BaseResource):
    _model_cls = UserModel
    _proxy = 'identity'
    _resource = 'users'
    _cloud_service_type_resource = cst.CLOUD_SERVICE_TYPE
    _cloud_service_meta = cs.CLOUD_SERVICE_METADATA
    _resource_path = "/identity/users/{id}/detail"
    _native_all_projects_query_support = False
    _native_project_id_query_support = False
    _associated_resource_cls_list = ['RoleResource', 'RoleAssignmentResource']

    def _find_role(self, user_id):

        role_assignments = self.get_resource_model_from_associated_resources('RoleAssignmentResource')

        role_id = None

        for role_assignment in role_assignments:
            if role_assignment.get('user') and role_assignment.get('user').get('id') == user_id and \
                    role_assignment.get('role'):
                role_id = role_assignment.get('role').get('id')

        if role_id:
            return self.get_resource_model_from_associated_resource('RoleResource', id=role_id)

        return None

    def _set_custom_model_obj_values(self, model_obj: UserModel, resource: Any):
        self._set_obj_key_value(model_obj, 'role', self._find_role(resource.id))


class RoleResource(BaseResource):
    _model_cls = RoleModel
    _proxy = 'identity'
    _resource = 'roles'
    _cloud_service_type_resource = CloudServiceTypeResource({"name": "Role", "group": "Identity"})


class RoleAssignmentResource(BaseResource):
    _model_cls = RoleAssignmentModel
    _proxy = 'identity'
    _resource = 'role_assignments'
    _cloud_service_type_resource = CloudServiceTypeResource({"name": "RoleAssignment", "group": "Identity"})
