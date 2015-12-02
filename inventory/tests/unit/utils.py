import unittest
import json
from inventory.tests import fixture, RequestMock
from inventory.utils import RequestHandler


class RequestHandlerTests(unittest.TestCase):

    def setUp(self):
        self.handler = RequestHandler()


if __name__ == '__main__':
    unittest.main()