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


class ShareNetwork(resource.Resource):
    resource_key = "share_network"
    resources_key = "share_networks"
    base_path = "/share-networks"

    # capabilities
    allow_create = False
    allow_fetch = False
    allow_commit = False
    allow_delete = False
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'name', 'project_id', all_projects='all_tenants')

    id = resource.Body("id")
    project_id = resource.Body("project_id")
    neutron_net_id = resource.Body("neutron_net_id")
    neutron_subnet_id = resource.Body("neutron_subnet_id")
    network_type = resource.Body("network_type")
    segmentation_id = resource.Body("segmentation_id", type=int)
    cidr = resource.Body("cidr")
    ip_version = resource.Body("ip_version")
    name = resource.Body("name")
    description = resource.Body("description")
    created_at = resource.Body("created_at")
    updated_at = resource.Body("updated_at")
    gateway = resource.Body("gateway")
    mtu = resource.Body("mtu")
    share_network_subnets = resource.Body("share_network_subnets", type=list)
    security_service_update_support = resource.Body("share_network_subnets", type=format.BoolStr)
    status = resource.Body("status")

    def _action(self, session, body):
        url = utils.urljoin(ShareNetwork.base_path, self.id, 'action')
        headers = {'Accept': ''}
        return session.post(url, json=body, headers=headers)

ShareNetworkDetail = ShareNetwork
