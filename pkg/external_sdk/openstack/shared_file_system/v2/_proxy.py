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

from openstack import proxy
from openstack.shared_file_system.v2 import availability_zone
from openstack.shared_file_system.v2 import share


class Proxy(proxy.Proxy):

    def availability_zones(self):
        """Retrieve shared file system availability zones

        :returns: A generator of availability zone resources
        :rtype: :class:`~openstack.shared_file_system.v2.
                                    \availability_zone.AvailabilityZone`
        """
        return self._list(availability_zone.AvailabilityZone)

    def shares(self, details=True, **query):
        """Retrieve a generator of volumes

        :param bool details: When set to ``False`` no extended attributes
            will be returned. The default, ``True``, will cause objects with
            additional attributes to be returned.
        :param kwargs query: Optional query parameters to be sent to limit
            the volumes being returned.  Available parameters include:

            * name: Name of the volume as a string.
            * all_projects: Whether return the volumes in all projects
            * status: Value of the status of the volume so that you can filter
                    on "available" for example.

        :returns: A generator of volume objects.
        """
        base_path = '/shares/detail' if details else None
        return self._list(share.Share, base_path=base_path, **query)
