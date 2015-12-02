import settings
import json
import unittest
import requests
from inventory.tests import fixture


class ApiTests(unittest.TestCase):

    def setUp(self):
        # Verify Server is running.
        # Verify Elastic Search is running.
        self.endpoint = 'http://{hostname}:{port}/v1/inventory'.format(
            hostname=settings.ELASTIC_URL,
            port=settings.ELASTIC_PORT)

    def test_valid_request(self):
        json_str = fixture('valid_request.json')
        data = json.loads(json_str)
        response = requests.post(self.endpoint + '/inventory', json=data)
        self.assertEquals(response.status_code, 201)

if __name__ == "__main__":
    unittest.main()