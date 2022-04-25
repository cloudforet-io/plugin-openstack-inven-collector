import time
import logging
import json
import concurrent.futures

from spaceone.core.service import *
from spaceone.inventory.conf.cloud_service_conf import *
from spaceone.inventory.model.common.response import ErrorResourceResponse
from spaceone.inventory import manager


from typing import (

    List,
    Dict,
    Optional,
    Union,
    Tuple,
    Callable,
    Iterator
)

__all__ = ['CollectorService']

_LOGGER = logging.getLogger(__name__)

@authentication_handler
class CollectorService(BaseService):

    def __init__(self, metadata):
        super().__init__(metadata)

        self.execute_managers = []


    #@check_required(['options'])
    def init(self, params) -> Dict:
        """ init plugin by options
        """
        _LOGGER.debug(params)
        capability = {
            'filter_format': FILTER_FORMAT,
            'supported_resource_type': SUPPORTED_RESOURCE_TYPE,
            'supported_features': SUPPORTED_FEATURES,
            'supported_schedules': SUPPORTED_SCHEDULES
        }
        return {'metadata': capability}

    @transaction
    #@check_required(['options', 'secret_data'])
    def verify(self, params) -> Dict:
        """
        Args:
              params:
                - options
                - secret_data
        """

        return {}

    @transaction
    @check_required(['options', 'secret_data'])
    def collect(self, params) -> Dict:
        """
        Args:
            params:
                - options
                - secret_data
                - filter
        """
        start_time = time.time()
        _LOGGER.debug(f'EXECUTOR START: Openstack Cloud Collector Service')
        # Get target manager to collect
        try:
            self.execute_managers = self._get_execute_managers(params.get('options', {}))
            _LOGGER.debug(f'[collect] execute_managers => {self.execute_managers}')
        except Exception as e:
            _LOGGER.error(f'[collect] failed to get target execute_managers => {e}', exc_info=True)
            error_response = self.generate_error_response(e, '', 'inventory.Error')
            yield error_response.to_primitive()

        # Execute manager
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
            future_executors = []
            for execute_manager in self.execute_managers:

                _manager = self.locator.get_manager(execute_manager)
                _LOGGER.debug(f'{_manager.__class__.__name__} module loaded')
                future_executors.append(executor.submit(_manager.collect_resources, params))

            for future in concurrent.futures.as_completed(future_executors):
                try:
                    for result in future.result():
                        yield result.to_primitive()
                except Exception as e:
                    _LOGGER.error(f'[collect] failed to yield result => {e}', exc_info=True)
                    error_response = self.generate_error_response(e, '', 'inventory.Error')
                    yield error_response.to_primitive()

        _LOGGER.debug(f'TOTAL TIME : {time.time() - start_time} Seconds')

    @staticmethod
    def _get_execute_managers(options) -> List['BaseManager']:
        return manager.list_manager()

    @staticmethod
    def generate_error_response(e, cloud_service_group, cloud_service_type) -> ErrorResourceResponse:
        if type(e) is dict:
            error_resource_response = ErrorResourceResponse({
                'message': json.dumps(e),
                'resource': {
                    'cloud_service_group': cloud_service_group,
                    'cloud_service_type': cloud_service_type
                }})
        else:
            error_resource_response = ErrorResourceResponse({
                'message': str(e),
                'resource': {
                    'cloud_service_group': cloud_service_group,
                    'cloud_service_type': cloud_service_type
                }})

        return error_resource_response
