import requests

from .exceptions import TransportError, HTTP_EXCEPTIONS


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
        try:
            response = self.session.send(request)
            raw_data = response.text
        except requests.ConnectionError as e:
            raise TransportError(e)

        if response.status_code >= 300:
            if response.status_code in HTTP_EXCEPTIONS:
                raise HTTP_EXCEPTIONS[response.status_code]()

            raise TransportError()
        return response.status_code, raw_data
