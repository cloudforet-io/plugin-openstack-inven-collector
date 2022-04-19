from spaceone.core.manager import BaseManager
from spaceone.inventory.model.common.region import RegionModel
from spaceone.inventory.model.common.response import RegionResponse
import time
import logging
import json
import os
import yaml
import errno

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


class RegionManager(BaseManager):
    region_file_path = 'metadata\\regions.yaml'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def _load_yaml_json_file(file_path: str) -> Dict:

        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    if file_path.endswith('json'):
                        return json.load(f)
                    else:
                        return yaml.safe_load(f)
            except IOError as e:
                # todo
                # exception
                raise
        else:
            #to do
            #default
            return {}


    @property
    def regions(self) -> Iterator[RegionModel]:

        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, self.region_file_path)

        regions = self._load_yaml_json_file(file_path)

        regions_dict = regions.get('regions')

        if regions_dict is None:
            # todo
            # exception
            raise

        for region_key, region_values in regions_dict.items():
            region_code = region_key
            region_name = region_values.get('name')
            region_tags = region_values.get('tags')

            yield RegionModel({'region_code': region_code, 'name': region_name, 'tags': region_tags})

    def collect_resources(self, params) -> Iterator[RegionResponse]:

        for region in self.regions:
            yield RegionResponse({'resource': region})


"""
    def collect_region(self):
        results = []
        for region_code in self.collected_region_codes:
            if region := self.match_region_info(region_code):
                results.append(RegionResponse({'resource': region}))

        return results

    def set_region_code(self, region):
        if region not in REGION_INFO:
            region = 'global'

        if region not in self.collected_region_codes:
            self.collected_region_codes.append(region)
"""
