import logging
from openstack.network.v2.security_group import SecurityGroup

from spaceone.inventory.manager.resources.metadata.cloud_service import security_group as cs
from spaceone.inventory.manager.resources.metadata.cloud_service_type import security_group as cst
from spaceone.inventory.manager.resources.resource import BaseResource
from spaceone.inventory.model.resources.security_group import SecurityGroupModel
from spaceone.inventory.model.resources.security_group import SecurityGroupRuleModel

_LOGGER = logging.getLogger(__name__)

class SecurityGroupResource(BaseResource):
    _model_cls = SecurityGroupModel
    _proxy = 'network'
    _resource = 'security_groups'
    _resource_path = "/auth/switch/{project_id}/?next=/project/security_groups/{id}"
    _cloud_service_type_resource = cst.CLOUD_SERVICE_TYPE
    _cloud_service_meta = cs.CLOUD_SERVICE_METADATA
    _native_all_projects_query_support = False
    _native_project_id_query_support = True

    def _set_custom_model_obj_values(self, model_obj: SecurityGroupModel, resource: SecurityGroup):

        if resource.get('security_group_rules'):
            security_group_rules = resource.security_group_rules
            security_group_rule_list = []

            for security_group_rule in security_group_rules:
                security_group_rule_list.append(SecurityGroupRuleModel(
                    {"id": security_group_rule.get('id'), "security_group_name": resource.get('name'),
                     "direction": security_group_rule.get('direction'),
                     "ethertype": security_group_rule.get('ethertype'),
                     "port_range_max": security_group_rule.get('port_range_max'),
                     "port_range_min": security_group_rule.get('port_range_min'),
                     "protocol": security_group_rule.get('protocol'),
                     "remote_ip_prefix": security_group_rule.get('remote_ip_prefix'),
                     "security_group_id": security_group_rule.get('security_group_id'),
                     "created_at": security_group_rule.get('created_at')
                     }))

            self._set_obj_key_value(model_obj, 'security_group_rules', security_group_rule_list)
