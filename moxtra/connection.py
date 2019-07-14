import json
import logging
import requests
import time

from .exceptions import TransportError, HTTP_EXCEPTIONS

logger = logging.getLogger('moxtra')


class Connection(object):
    transport_schema = 'https'

    def __init__(self, production, *args, **kwargs):
        self.host = ("https://api.moxtra.com/" if production
                     else "https://apisandbox.moxtra.com/")


class RequestsHttpsConnection(Connection):
    def __init__(self, production=False, *args, **kwargs):
        super(RequestsHttpsConnection, self).__init__(production,
                                                      *args,
                                                      **kwargs)
        self.session = requests.session()

    def perform_request(self, method, url,
                        params=None, body=None):
        url = self.host + url

        request = requests.Request(method, url,
                                   params=params or {}, data=body).prepare()
        start = time.time()
        try:
            response = self.session.send(request)
            duration = time.time() - start
            raw_data = response.text
        except requests.ConnectionError as e:
            raise TransportError(e)

        if not (200 <= response.status_code < 300):
            if response.status_code in HTTP_EXCEPTIONS:
                raise HTTP_EXCEPTIONS[response.status_code]()

            raise TransportError()
        self.log_request_success(method, request.url, request.path_url, body,
                                 response.status_code, raw_data, duration)
        return response.status_code, raw_data

    def log_request_success(self, method,
                            full_url, path,
                            body, status_code,
                            response, duration):
        def _pretty_json(data):
            data = json.dumps(json.loads(data), sort_keys=True,
                              indent=2, separators=(', ', ': '))
            return data

        logger.info('%s %s [status: %s request: %.3fs]', method, full_url,
                    status_code, duration)
        logger.debug('> %s', body)
        logger.debug('< %s', response)
