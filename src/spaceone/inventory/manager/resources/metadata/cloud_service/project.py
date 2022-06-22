from spaceone.inventory.manager.resources.metadata.cloud_service_type.project import CST_PROJECT_META
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.view.cloud_service import CloudServiceMeta
from spaceone.inventory.model.view.dynamic_layout import ItemDynamicLayout, TableDynamicLayout

CS_PROJECT_META = CSTMetaGenerator(CST_PROJECT_META)

CS_PROJECT_META.append_cst_meta_field('TextDyField', 'ID', 'data.id', index=0)
CS_PROJECT_META.insert_cst_meta_field('ID', 'TextDyField', 'Name', 'data.name')
CS_PROJECT_META.append_cst_meta_field('TextDyField', 'Option', 'data.options')
CS_PROJECT_META.append_cst_meta_field('TextDyField', 'externalLink', 'data.external_link')

CLOUD_SERVICE_BASE = ItemDynamicLayout.set_fields('Project', fields=CS_PROJECT_META.fields)
CLOUD_SERVICE_METADATA = CloudServiceMeta.set_layouts(layouts=[CLOUD_SERVICE_BASE])

CS_PROJECT_QUOTA_META = CSTMetaGenerator()
CS_PROJECT_QUOTA_META.append_cst_meta_field('TextDyField', 'Name', 'name')
CS_PROJECT_QUOTA_META.append_cst_meta_field('TextDyField', 'Limit', 'limit')
CS_PROJECT_QUOTA_META.append_cst_meta_field('TextDyField', 'In Use', 'in_use')
CS_PROJECT_QUOTA_META.append_cst_meta_field('TextDyField', 'Reserved', 'reserved')
CS_PROJECT_QUOTA_META.append_cst_meta_field('EnumDyField', 'Type', 'quota_type',
                                            default_badge={
                                                'coral.600': ['Compute'], 'indigo.500': ['Network'],
                                                'peacock.500': ['Volume'], 'violet.500': ['Share']}
                                            )

CLOUD_SERVICE_PROJECT_QUOTA = TableDynamicLayout.set_fields('Quota', root_path="data.quota_sets",
                                                            fields=CS_PROJECT_QUOTA_META.fields)

CLOUD_SERVICE_METADATA = CloudServiceMeta.set_layouts(layouts=[CLOUD_SERVICE_BASE, CLOUD_SERVICE_PROJECT_QUOTA])
