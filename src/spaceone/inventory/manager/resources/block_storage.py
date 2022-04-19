from spaceone.inventory.model.block_storage.data import VolumeModel
from spaceone.inventory.manager.resources.resource import BaseResource
from spaceone.inventory.model.common.base import ReferenceModel
from openstack.block_storage.v2.volume import Volume

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


class VolumeResource(BaseResource):
    _model_cls = VolumeModel
    _proxy = 'block_storage'
    _resource = 'volumes'

    @property
    def resources(self) -> List[Volume]:
        return super().resources

    def _set_default_model_obj_values(self, model_obj: VolumeModel, resource: Volume):

        if hasattr(resource, 'location') and hasattr(resource.location, 'region_name'):
            self._set_obj_key_value(model_obj, 'region_name', resource.location.region_name)

        if hasattr(resource, 'attachments') and len(resource.attachments) > 1:
            self._set_obj_key_value(model_obj, 'multiattach', True)

        if hasattr(resource, 'links'):
            dic = {}

            for link in resource.links:
                if link['rel'] == 'self':
                    dic['self_link'] = link['href']

                if link['rel'] == 'bookmark':
                    dic['bookmark_link'] = link['href']

            self._set_obj_key_value(model_obj, 'reference', ReferenceModel(dic))
