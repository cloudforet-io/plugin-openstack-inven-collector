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

from openstack import resource


class ResourceProvider(resource.Resource):
    resource_key = None
    resources_key = 'resource_providers'
    base_path = '/resource_providers'

    # Capabilities

    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True

    # Filters

    _query_mapping = resource.QueryParameters(
        'name', 'member_of', 'resources', 'in_tree', 'required', id='uuid',
    )

    # The parent_provider_uuid and root_provider_uuid fields were introduced in
    # 1.14
    # The required query parameter was added in 1.18
    # The create operation started returning a body in 1.20
    _max_microversion = '1.20'

    # Properties

    #: The UUID of a resource provider.
    id = resource.Body('uuid', alternate_id=True)
    #: A consistent view marker that assists with the management of concurrent
    #: resource provider updates.
    generation = resource.Body('generation')
    #: Links pertaining to this flavor. This is a list of dictionaries,
    #: each including keys ``href`` and ``rel``.
    links = resource.Body('links')
    #: The name of this resource provider.
    name = resource.Body('name')
    #: The UUID of the immediate parent of the resource provider.
    parent_provider_id = resource.Body('parent_provider_uuid')
    #: Read-only UUID of the top-most provider in this provider tree.
    root_provider_id = resource.Body('root_provider_uuid')


class ResourceProviderInventory(resource.Resource):
    resource_key = None
    resources_key = None
    base_path = '/resource_providers'

    allow_fetch = True
    # Filters

    _query_mapping = resource.QueryParameters(
        id='uuid',
    )

    _min_microversion = '1.5'
    #: The UUID of a resource provider.
    resource_provider_generation = resource.Body('resource_provider_generation')
    #: A consistent view marker that assists with the management of concurrent
    #: resource provider updates.
    inventories = resource.Body('inventories')


class ResourceProviderUsage(resource.Resource):
    resource_key = None
    resources_key = None
    base_path = '/resource_providers'

    allow_fetch = True
    # Filters

    _query_mapping = resource.QueryParameters(
        id='uuid',
    )

    _min_microversion = '1.9'
    #: The UUID of a resource provider.
    resource_provider_generation = resource.Body('resource_provider_generation')
    #: A consistent view marker that assists with the management of concurrent
    #: resource provider updates.
    usages = resource.Body('usages')