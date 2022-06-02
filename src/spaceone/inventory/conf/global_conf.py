# Database Settings

import logging
import os
import json
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


DATABASES = {
    'default': {
        # MongoDB Example
        # 'host': '<host>',
        # 'port': 27017,
        # 'db': '<db>',
        # 'username': '<user>',
        # 'password': '<password>'
    },
    # 'local': {
    #     'backend': 'spaceone.core.cache.local_cache.LocalCache',
    #     'max_size': 128,
    #     'ttl': 86400
    # }
}

# Cache Settings
CACHES = {
    'default': {
        # Redis Example
        # 'backend': 'spaceone.core.cache.redis_cache.RedisCache',
        # 'host': '<host>',
        # 'port': 6379,
        # 'db': 0
    }
}

# Handler Configuration
HANDLERS = {
    'authentication': [
        # Default Authentication Handler
        # {
        #     'backend': 'spaceone.core.handler.authentication_handler.AuthenticationGRPCHandler',
        #     'uri': 'grpc://identity:50051/v1/Domain/get_public_key'
        # }
    ],
    'authorization': [
        # Default Authorization Handler
        # {
        #     'backend': 'spaceone.core.handler.authorization_handler.AuthorizationGRPCHandler',
        #     'uri': 'grpc://identity:50051/v1/Authorization/verify'
        # }
    ],
    'mutation': [],
    'event': []
}

# Connector Settings
CONNECTORS = {
}

# Log Settings
LOG = {
    'filters': {
        'masking': {
            'rules': {
                'Collector.collect': [
                    'secret_data'
                ]
            }
        }
    }
}
