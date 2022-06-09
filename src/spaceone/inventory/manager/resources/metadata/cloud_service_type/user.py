import os

from spaceone.inventory.libs.common_parser import get_data_from_yaml
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.common.response import CloudServiceTypeResource
from spaceone.inventory.model.view.cloud_service_type import CloudServiceTypeMeta
from spaceone.inventory.model.view.dynamic_field import TextDyField, EnumDyField, DateTimeDyField, BadgeDyField
from spaceone.inventory.model.view.dynamic_widget import ChartWidget, CardWidget

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/user/total_count.yml')
count_by_region_conf = os.path.join(current_dir, 'widget/user/count_by_region.yml')

CLOUD_SERVICE_TYPE = CloudServiceTypeResource()
CLOUD_SERVICE_TYPE.provider = 'openstack'
CLOUD_SERVICE_TYPE.name = 'User'
CLOUD_SERVICE_TYPE.group = 'Identity'
CLOUD_SERVICE_TYPE.labels = ['Identity', 'User']
CLOUD_SERVICE_TYPE.is_primary = True
CLOUD_SERVICE_TYPE.is_major = True
CLOUD_SERVICE_TYPE.service_code = 'OSUser'
CLOUD_SERVICE_TYPE.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/openstack/openstack_identity.svg',
    'spaceone:display_name': 'User'
}

CST_USER_META = CSTMetaGenerator()
CST_USER_META.append_cst_meta_field(TextDyField, 'Name', 'data.name')
CST_USER_META.append_cst_meta_field(BadgeDyField, 'ID', 'data.id', auto_search=True,
                                    reference={"resource_type": "inventory.CloudService",
                                               "reference_key": "reference.resource_id"},
                                    options={'is_optional': True})
CST_USER_META.append_cst_meta_field(EnumDyField, 'Enabled', 'data.is_enabled', auto_search=True,
                                    default_badge={'indigo.500': ['true'], 'coral.600': ['false']})
CST_USER_META.append_cst_meta_field(TextDyField, 'Role ID', 'data.role.id', auto_search=True,
                                    options={'is_optional': True})
CST_USER_META.append_cst_meta_field(EnumDyField, 'Role Name', 'data.role.name', auto_search=True,
                                    default_badge={
                                        'coral.600': ['admin'], 'indigo.500': ['_member_'], 'peacock.500': ['member'],
                                        'green.500': ['reader'], 'red.500': ['heat_stack_user'],
                                        'violet.500': ['heat_stack_owner'], })
CST_USER_META.append_cst_meta_field(TextDyField, 'Email', 'data.email', auto_search=True)
CST_USER_META.append_cst_meta_field(DateTimeDyField, 'Password Expire', 'data.password_expires_at', auto_search=True)
CST_USER_META.append_cst_meta_field(BadgeDyField, 'Default Project Id', 'data.default_project_id', auto_search=True,
                                    reference={"resource_type": "inventory.CloudService",
                                               "reference_key": "reference.resource_id"})
CST_USER_META.append_cst_meta_field(TextDyField, 'Domain ID', 'data.domain_id', auto_search=True)


CLOUD_SERVICE_TYPE._metadata = CloudServiceTypeMeta.set_meta(
    fields=CST_USER_META.fields, search=CST_USER_META.search,
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_region_conf)),
    ]
)
