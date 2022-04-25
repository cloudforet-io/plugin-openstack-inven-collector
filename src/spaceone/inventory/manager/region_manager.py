from spaceone.core.manager import BaseManager
from spaceone.inventory.model.common.region import RegionModel
from spaceone.inventory.model.common.response import RegionResponse
from spaceone.inventory.libs import common_parser
from spaceone.inventory.error.base import CollectorError

import json
import os
import yaml
import errno
import logging

from typing import (
    Any,
    Iterator,
    List,
    Dict,
    Optional,
    Type,
    Union,
    Tuple,
)

_LOGGER = logging.getLogger(__name__)


class RegionManager(BaseManager):
    region_file_path = 'metadata/regions.yaml'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def regions(self) -> Iterator[RegionModel]:

        current_dir = os.path.abspath(os.path.dirname(__file__))
        _LOGGER.debug(f"Current Directory is {current_dir}")

        file_path = os.path.join(current_dir, self.region_file_path)

        _LOGGER.debug(f"Loading .. {file_path}")
        regions = common_parser.load_yaml_json_file(file_path)

        regions_dict = regions.get('regions')

        if regions_dict is None:
            raise CollectorError(message=f"Region data not exists in {file_path}")

        _LOGGER.debug(f"Region data is {regions_dict}")

        for region_key, region_values in regions_dict.items():
            region_name = region_values.get('name')
            region_tags = region_values.get('tags')

            yield RegionModel({'region_code': region_key, 'name': region_name, 'tags': region_tags})

    def collect_resources(self, params: Dict = {}) -> Iterator[RegionResponse]:

        for region in self.regions:
            yield RegionResponse({'resource': region})
