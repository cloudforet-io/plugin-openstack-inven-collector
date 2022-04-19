from spaceone.inventory.model.compute.data import InstanceModel
from spaceone.inventory.model.compute.data import FlavorModel
from spaceone.inventory.model.common.base import ReferenceModel
from spaceone.inventory.manager.resources.resource import BaseResource
from openstack.compute.v2.server import Server
from openstack.compute.v2.flavor import Flavor
import copy

from typing import (
    Any,
    Iterable,
    List,
    Dict,
    Optional,
    Type,
    Union,
    Tuple,
    Iterator
)


class InstanceResource(BaseResource):
    _model_cls = InstanceModel
    _proxy = 'compute'
    _resource = 'servers'

    @property
    def resources(self) -> List[Server]:
        return super().resources

    def _set_default_model_obj_values(self, model_obj: InstanceModel, resource: Server):

        ## insert custom data
        if hasattr(resource, 'location') and hasattr(resource.location, 'region_name'):
            self._set_obj_key_value(model_obj, 'region_name', resource.location.region_name)

        if hasattr(resource, 'links'):
            dic = {}

            links = resource.links

            for link in links:
                if link['rel'] == 'self':
                    dic['self_link'] = link['href']

                if link['rel'] == 'bookmark':
                    dic['bookmark_link'] = link['href']

            self._set_obj_key_value(model_obj, 'reference', ReferenceModel(dic))

        if hasattr(resource, 'flavor'):

            dic = resource.flavor

            if 'original_name' in dic:
                dic['name'] = dic['original_name']
                del dic['original_name']

            self._set_obj_key_value(model_obj, 'flavor', FlavorModel(dic))


class FlavorResource(BaseResource):
    _model_cls = FlavorModel
    _proxy = 'compute'
    _resource = 'flavors'

