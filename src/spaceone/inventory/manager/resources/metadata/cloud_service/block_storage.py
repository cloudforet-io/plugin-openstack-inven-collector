from spaceone.inventory.manager.resources.metadata.cloud_service_type.block_storage import CST_VOLUME_META
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.view.cloud_service import CloudServiceMeta
from spaceone.inventory.model.view.dynamic_field import TextDyField, DateTimeDyField
from spaceone.inventory.model.view.dynamic_layout import ItemDynamicLayout, TableDynamicLayout

CS_VOLUME_META = CSTMetaGenerator(CST_VOLUME_META)

CS_VOLUME_META.insert_cst_meta_field('ID', TextDyField, 'Description', 'data.description')
CS_VOLUME_META.insert_cst_meta_field('Size(GiB)', TextDyField, 'Size(Byte)', 'data.size')
CS_VOLUME_META.append_cst_meta_field(TextDyField, 'selfLink', 'data.reference.self_link')
CS_VOLUME_META.append_cst_meta_field(TextDyField, 'bookmarkLink', 'data.reference.bookmark_link')
CS_VOLUME_META.append_cst_meta_field(TextDyField, 'externalLink', 'data.external_link')

CS_VOLUME_ATTACHMENTS_META = CSTMetaGenerator()
CS_VOLUME_ATTACHMENTS_META.append_cst_meta_field(TextDyField, 'ID', 'id')
CS_VOLUME_ATTACHMENTS_META.append_cst_meta_field(TextDyField, 'Instance ID', 'server_id',
                                                 reference={"resource_type": "inventory.CloudService",
                                                            "reference_key": "reference.resource_id"})
CS_VOLUME_ATTACHMENTS_META.append_cst_meta_field(TextDyField, 'Device', 'device')
CS_VOLUME_ATTACHMENTS_META.append_cst_meta_field(TextDyField, 'Host name', 'host_name')
CS_VOLUME_ATTACHMENTS_META.append_cst_meta_field(TextDyField, 'Attachment ID', 'attachment_id')
CS_VOLUME_ATTACHMENTS_META.append_cst_meta_field(DateTimeDyField, 'Attached', 'attached_at')

CLOUD_SERVICE_BASE = ItemDynamicLayout.set_fields('Volume', fields=CS_VOLUME_META.fields)

CLOUD_SERVICE_ATTACHMENT = TableDynamicLayout.set_fields('Attachments', fields=CS_VOLUME_ATTACHMENTS_META.fields,
                                                         root_path="data.attachments")

CLOUD_SERVICE_METADATA = CloudServiceMeta.set_layouts(layouts=[CLOUD_SERVICE_BASE, CLOUD_SERVICE_ATTACHMENT])
