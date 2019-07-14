from unittest import TestCase
from mock import Mock

from moxtra.connection import RequestsHttpsConnection


class TestRequestsConnection(TestCase):
    def _get_mock_connection(self, connection_params={},
                             status_code=200,
                             response_body=u'{}'):
        conn = RequestsHttpsConnection(**connection_params)
        conn.session.send = Mock()
        dummy_response = Mock()
        conn.session.send.return_value = dummy_response
        dummy_response.status_code = status_code
        dummy_response.text = response_body
        return conn

    def _get_request(self, connection, *args, **kwargs):
        status, data = connection.perform_request(*args,
                                                  **kwargs)
        self.assertEquals(200, status)
        self.assertEquals(u'{}', data)
        self.assertEquals(1, connection.session.send.call_count)
        args, kwargs = connection.session.send.call_args
        self.assertEquals({}, kwargs)
        self.assertEquals(1, len(args))
        return args[0]

    def test_defaults(self):
        conn = self._get_mock_connection()
        request = self._get_request(conn, 'GET', '')

        self.assertEquals('https://apisandbox.moxtra.com/', request.url)
        self.assertEquals('GET', request.method)
        self.assertEquals(None, request.body)

    def test_body_attached(self):
        conn = self._get_mock_connection()
        request = self._get_request(conn, 'GET', '', body="{'answer': 42}")

        self.assertEquals('https://apisandbox.moxtra.com/', request.url)
        self.assertEquals('GET', request.method)
        self.assertEquals("{'answer': 42}", request.body)
