# Database Settings

import json
import logging
import os

from spaceone.inventory.error.base import CollectorError

_LOGGER = logging.getLogger(__name__)

DEBUG_ENABLED: bool = False
DEFAULT_LOG_LEVEL = logging.INFO

try:
    OS_DEBUG_ENABLED = os.getenv("DEBUG_ENABLED")
    if OS_DEBUG_ENABLED is None:
        raise CollectorError("DEBUG_ENABLED ENV not set. Default log level is INFO")
    DEBUG_ENABLED = json.loads(OS_DEBUG_ENABLED.lower())
except Exception as e:
    _LOGGER.error(e)

if DEBUG_ENABLED:
    DEFAULT_LOG_LEVEL = logging.DEBUG


def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(DEFAULT_LOG_LEVEL)
    return logger
