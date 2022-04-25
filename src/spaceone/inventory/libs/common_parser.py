import logging
import json
import os
import yaml
from spaceone.inventory.error.base import CollectorError

from typing import (
    Dict,
)

_LOGGER = logging.getLogger(__name__)


def get_data_from_yaml(file_path):
    return load_yaml_json_file(file_path)


def load_yaml_json_file(file_path: str) -> Dict:
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                if file_path.endswith('json'):
                    return json.load(f)
                else:
                    return yaml.safe_load(f)
        except Exception as e:
            raise CollectorError(message=f"Loading {file_path} failed.", cause=e)
    else:
        raise CollectorError(message=f"{file_path} not exist.")