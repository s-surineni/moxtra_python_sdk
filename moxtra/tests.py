import ConfigParser
import os
import unittest

from .client import Client


parser = ConfigParser.ConfigParser()
config_file_path = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), 'config.ini')

parser.read(config_file_path)
client_details = parser.items('local')
client_id = client_details[0][1]
client_secret = client_details[1][1]

cl = Client(client_id, client_secret)


class TestMoxtraApi(unittest.TestCase):
    def setUp(self):
        self.moxtra_client = Client(
            client_id,
            client_secret)

    def test_get_access_token(self):
        result = self.moxtra_client.get_access_token()
        assert result.get('access_token') is not None


if __name__ == '__main__':
    unittest.main()
