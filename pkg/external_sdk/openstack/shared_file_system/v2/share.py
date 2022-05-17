# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from openstack import format
from openstack import resource
from openstack import utils

class Share(resource.Resource):
    resource_key = "share"
    resources_key = "shares"
    base_path = "/shares"

    # capabilities
    allow_create = False
    allow_fetch = False
    allow_commit = False
    allow_delete = False
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'name', 'status', 'project_id', all_projects='all_tenants')

    # Properties
    #: A ID representing this volume.
    id = resource.Body("id")
    #: The name of this volume.
    name = resource.Body("name")
    #: A list of links associated with this volume. *Type: list*
    links = resource.Body("links", type=list)

    size = resource.Body("size", type=int)
    availability_zone = resource.Body("availability_zone")
    created_at = resource.Body("created_at")
    status = resource.Body("status")
    description = resource.Body("description")
    project_id = resource.Body("project_id")
    snapshot_id = resource.Body("snapshot_id")
    share_network_id = resource.Body("share_network_id")
    share_proto = resource.Body("share_proto")
    metadata = resource.Body("metadata")
    share_type = resource.Body("share_type")
    is_public = resource.Body("is_public", type=format.BoolStr)
    share_server_id = resource.Body("share_server_id")
    host = resource.Body("host")
    snapshot_support = resource.Body("snapshot_support", type=format.BoolStr)
    task_state = resource.Body("task_state")
    share_type_name = resource.Body("share_type_name")
    access_rules_status = resource.Body("access_rules_status")
    replication_type = resource.Body("replication_type")
    has_replicas = resource.Body("replication_type", type=format.BoolStr)
    user_id = resource.Body("user_id")
    create_share_from_snapshot_support = resource.Body("create_share_from_snapshot_support", type=format.BoolStr)
    revert_to_snapshot_support = resource.Body("revert_to_snapshot_support", type=format.BoolStr)
    share_group_id = resource.Body("share_group_id")
    source_share_group_snapshot_member_id = resource.Body("source_share_group_snapshot_member_id")
    mount_snapshot_support = resource.Body("mount_snapshot_support")
    progress = resource.Body("progress")
    count = resource.Body("count", type=int)
    volume_type = resource.Body("volume_type")
    export_location = resource.Body("export_location")
    export_locations = resource.Body("export_locations", type=list)
    is_soft_deleted  = resource.Body("is_soft_deleted ", type=format.BoolStr)
    scheduled_to_be_deleted_at = resource.Body("export_location")


    def _action(self, session, body):
        """Preform volume actions given the message body."""
        # NOTE: This is using Share.base_path instead of self.base_path
        # as both Share and ShareDetail instances can be acted on, but
        # the URL used is sans any additional /detail/ part.
        url = utils.urljoin(Volume.base_path, self.id, 'action')
        headers = {'Accept': ''}
        return session.post(url, json=body, headers=headers)


ShareDetail = Share
