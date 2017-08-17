import unittest

from smartobjects.api_manager import APIManager, ServiceUnavailable
from smartobjects.smartobjects_client import ExponentialBackoffConfig
from smartobjects.model import *
from smartobjects.model.model import ModelService
from tenacity import RetryError

from tests.mocks.local_api_server import LocalApiServer


class TestBackoff(unittest.TestCase):
    """
    Retry on 503 response
    """

    @classmethod
    def setUpClass(cls):
        cls.server = LocalApiServer()
        cls.server.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def setUp(self):
        self.server.server.backend.clear()

    def test_retry_default(self):
        config = ExponentialBackoffConfig()
        api = APIManager("CLIENT_ID", "CLIENT_SECRET", self.server.path, compression_enabled=False, backoff_config = config, token_override=None)
        value = api.get('unvailable/1')
        self.assertEqual(value.json()['data'], "ok")

    def test_retry_until_200(self):
        self.counter = 0
        def on_retry(func, trial_number):
            self.counter = self.counter + 1
        config = ExponentialBackoffConfig(5, 0.5, on_retry)
        api = APIManager("CLIENT_ID", "CLIENT_SECRET", self.server.path, compression_enabled=False, backoff_config = config, token_override=None)
        value = api.get('unvailable/3')
        self.assertEqual(self.counter, 4)
        self.assertEqual(value.json()['data'], "ok")

    def test_retry_until_limit(self):
        self.counter = 0
        def on_retry(func, trial_number):
            self.counter = self.counter + 1
        config = ExponentialBackoffConfig(5, 0.1, on_retry)
        api = APIManager("CLIENT_ID", "CLIENT_SECRET", self.server.path, compression_enabled=False, backoff_config = config, token_override=None)
        with self.assertRaises(ServiceUnavailable) as ctx:
            api.get('unvailable/100')
        self.assertEqual(self.counter, 5)

    def test_do_not_retry_if_success(self):
        api = APIManager("CLIENT_ID", "CLIENT_SECRET", self.server.path, compression_enabled=False, backoff_config = None, token_override=None)
        value = api.get('unvailable/0')
        self.assertEqual(value.json()['data'], "ok")