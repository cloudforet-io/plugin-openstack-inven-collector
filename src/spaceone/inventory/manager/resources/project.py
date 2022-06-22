from spaceone.inventory.manager.resources.metadata.cloud_service import project as cs
from spaceone.inventory.manager.resources.metadata.cloud_service_type import project as cst
from spaceone.inventory.manager.resources.resource import BaseResource
from spaceone.inventory.model.resources.project import ProjectModel


class ProjectResource(BaseResource):
    _model_cls = ProjectModel
    _proxy = 'identity'
    _resource = 'projects'
    _cloud_service_type_resource = cst.CLOUD_SERVICE_TYPE
    _cloud_service_meta = cs.CLOUD_SERVICE_METADATA
    _resource_path = "/identity"
    _native_all_projects_query_support = False
    _native_project_id_query_support = False
    _associated_resource_cls_list = ['ComputeQuotaResource', 'VolumeQuotaResource']

    def _set_custom_model_obj_values(self, model_obj: ProjectModel, resource):

        quota_set_list = []
        project_id = resource.id

        compute_quota_set_detail = self.get_resource_model_from_associated_resource('ComputeQuotaResource',
                                                                                    id=project_id)
        volume_quota_set_detail = self.get_resource_model_from_associated_resource('VolumeQuotaResource', id=project_id)

        if compute_quota_set_detail:

            compute_quota_set_detail = compute_quota_set_detail.to_primitive()

            for key, value in compute_quota_set_detail.items():

                if isinstance(value, dict):

                    quota_set = {
                        "name": key,
                        "project_id": project_id,
                        "quota_type": compute_quota_set_detail.get('quota_type'),
                    }

                    if compute_quota_set_detail.get(key):
                        compute_quota_set_detail_key = compute_quota_set_detail.get(key)
                        quota_set['in_use'] = compute_quota_set_detail_key.get('in_use')
                        quota_set['limit'] = compute_quota_set_detail_key.get('limit')
                        quota_set['reserved'] = compute_quota_set_detail_key.get('reserved')

                    quota_set_list.append(quota_set)

        if volume_quota_set_detail:

            volume_quota_set_detail = volume_quota_set_detail.to_primitive()

            search_keys = ["backup_gigabytes", "backups", "gigabytes", "groups", "per_volume_gigabytes", "snapshots",
                           "volumes"]

            for search_key in search_keys:
                quota_set = {
                    "name": search_key,
                    "project_id": project_id,
                    "quota_type": volume_quota_set_detail.get('quota_type'),
                    "limit": volume_quota_set_detail.get(search_key),
                }

                if volume_quota_set_detail.get('usage'):
                    usage = volume_quota_set_detail.get('usage')
                    quota_set["in_use"] = usage.get(search_key)

                if volume_quota_set_detail.get('reservation'):
                    reservation = volume_quota_set_detail.get('reservation')
                    quota_set["reserved"] = reservation.get(search_key)

                quota_set_list.append(quota_set)

        self._set_obj_key_value(model_obj, 'quota_sets', quota_set_list)
