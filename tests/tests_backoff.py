import unittest
from typing import Callable

from smartobjects.api_manager import APIManager, ServiceUnavailable
from smartobjects.smartobjects_client import ExponentialBackoffConfig
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
        api = APIManager("CLIENT_ID", "CLIENT_SECRET", self.server.path, compression_enabled=False,
                         backoff_config=config, token_override=None)
        value = api.get('/api/v3/unvailable/1')
        self.assertEqual(value.json()['data'], "ok")

    def test_retry_until_200(self):
        self.counter = 0

        def on_retry(func: Callable, trial_number: int):
            self.counter = self.counter + 1

        config = ExponentialBackoffConfig(5, 0.5, on_retry)
        api = APIManager("CLIENT_ID", "CLIENT_SECRET", self.server.path, compression_enabled=False,
                         backoff_config=config, token_override=None)
        value = api.get('/api/v3/unvailable/3')
        self.assertEqual(self.counter, 4)
        self.assertEqual(value.json()['data'], "ok")

    def test_retry_until_limit(self):
        self.counter = 0

        def on_retry(func: Callable, trial_number: int):
            self.counter = self.counter + 1

        config = ExponentialBackoffConfig(5, 0.1, on_retry)
        api = APIManager("CLIENT_ID", "CLIENT_SECRET", self.server.path, compression_enabled=False,
                         backoff_config=config, token_override=None)
        with self.assertRaises(ServiceUnavailable) as ctx:
            api.get('/api/v3/unvailable/100')
        self.assertEqual(self.counter, 5)

    def test_do_not_retry_if_success(self):
        api = APIManager("CLIENT_ID", "CLIENT_SECRET", self.server.path, compression_enabled=False, backoff_config=None,
                         token_override=None)
        value = api.get('/api/v3/unvailable/0')
        self.assertEqual(value.json()['data'], "ok")
