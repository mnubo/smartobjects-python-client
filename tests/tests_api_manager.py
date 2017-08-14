import unittest
from requests import Response
import datetime

from smartobjects import APIManager
from tests.mocks.local_api_server import LocalApiServer


class TestsApiManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = LocalApiServer()
        cls.server.start()
        cls.api = APIManager("CLIENT_ID", "CLIENT_SECRET", cls.server.path, compression_enabled=False, backoff_config = None)

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def setUp(self):
        self.server.server.backend.clear()

    def tests_host_non_reachable(self):
        with self.assertRaises(ValueError) as ctx:
            APIManager("CLIENT_ID", "CLIENT_SECRET", "http://non-reachable.example.com", compression_enabled=False, backoff_config = None)
            self.assertEqual(ctx.exception.message, "Host at {} is not reachable".format("http://non-reachable.example.com"))

    def test_client_id_null(self):
        with self.assertRaises(ValueError) as ctx:
            APIManager("", "CLIENT_SECRET", self.server.path, compression_enabled=False, backoff_config = None)
            self.assertEqual(ctx.exception.message, "client_id cannot be null or empty.")

    def test_client_secret_null(self):
        with self.assertRaises(ValueError) as ctx:
            APIManager("CLIENT_ID", "", self.server.path, compression_enabled=False, backoff_config = None)
            self.assertEqual(ctx.exception.message, "client_secret cannot be null or empty.")

    def test_fetch_token_at_init(self):
        api = APIManager("CLIENT_ID", "CLIENT_SECRET", self.server.path, compression_enabled=False, backoff_config = None)
        self.assertIn("access_token", api.access_token)
        self.assertIn("expires_in", api.access_token)
        self.assertIn("requested_at", api.access_token)

    def test_get_api_url(self):
        url = self.api.get_api_url()
        self.assertEqual(url, "{}/api/v3/".format(self.server.path))

    def test_token_is_valid(self):
        api = APIManager("CLIENT_ID", "CLIENT_SECRET", self.server.path, compression_enabled=False, backoff_config = None)
        self.assertTrue(api.is_access_token_valid())

    def test_token_invalid(self):
        api = APIManager("CLIENT_ID", "CLIENT_SECRET", self.server.path, compression_enabled=False, backoff_config = None)
        api.access_token['requested_at'] = datetime.datetime.now() - datetime.timedelta(hours=2)
        self.assertFalse(api.is_access_token_valid())

    def test_refresh_token(self):
        api = APIManager("CLIENT_ID", "CLIENT_SECRET", self.server.path, compression_enabled=False, backoff_config = None)
        api.access_token['requested_at'] = datetime.datetime.now() - datetime.timedelta(hours=2)
        self.assertFalse(api.is_access_token_valid())

        api.get("api_manager?parameter")
        self.assertTrue(api.is_access_token_valid())

    def test_raise_valueerror_on_400(self):
        r = Response()
        r.status_code = 400
        r._content = "error message"

        with self.assertRaises(ValueError) as ctx:
            self.api.validate_response(r)
            self.assertEqual(ctx.exception.message, "error message")

    def test_get(self):
        r = self.api.get("api_manager?parameter")

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.request.method, 'GET')
        self.assertEqual(r.request.path_url, '/api/v3/api_manager?parameter')
        self.assertIn('parameter', r.json())

    def test_post(self):
        r = self.api.post("api_manager?parameter", {"data": "value"})

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.request.method, 'POST')
        self.assertEqual(r.request.path_url, '/api/v3/api_manager?parameter')
        self.assertIn('parameter', r.json()[0])
        self.assertEqual({"data": "value"}, r.json()[1])

    def test_put(self):
        r = self.api.put("api_manager?parameter", {"data": "value"})

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.request.method, 'PUT')
        self.assertEqual(r.request.path_url, '/api/v3/api_manager?parameter')
        self.assertIn('parameter', r.json()[0])
        self.assertEqual({"data": "value"}, r.json()[1])

    def test_delete(self):
        r = self.api.delete("api_manager?parameter")

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.request.method, 'DELETE')
        self.assertEqual(r.request.path_url, '/api/v3/api_manager?parameter')
        self.assertIn('parameter', r.json()[0])

    def test_authorization_token(self):
        r = self.api.get("api_manager")
        self.assertIn('Authorization', r.request.headers)
        self.assertTrue(r.request.headers['Authorization'].startswith('Bearer'))

        r = self.api.post("api_manager", {})
        self.assertIn('Authorization', r.request.headers)
        self.assertTrue(r.request.headers['Authorization'].startswith('Bearer'))

        r = self.api.put("api_manager", {})
        self.assertIn('Authorization', r.request.headers)
        self.assertTrue(r.request.headers['Authorization'].startswith('Bearer'))

        r = self.api.delete("api_manager")
        self.assertIn('Authorization', r.request.headers)
        self.assertTrue(r.request.headers['Authorization'].startswith('Bearer'))

    def test_content_type(self):
        r = self.api.get("api_manager")
        self.assertIn('Content-Type', r.request.headers)
        self.assertEqual('application/json', r.request.headers['Content-Type'])

        r = self.api.post("api_manager", {})
        self.assertIn('Content-Type', r.request.headers)
        self.assertEqual('application/json', r.request.headers['Content-Type'])

        r = self.api.put("api_manager", {})
        self.assertIn('Content-Type', r.request.headers)
        self.assertEqual('application/json', r.request.headers['Content-Type'])

        r = self.api.delete("api_manager")
        self.assertIn('Content-Type', r.request.headers)
        self.assertEqual('application/json', r.request.headers['Content-Type'])

    def test_accept_encoding(self):
        r = self.api.get("api_manager")
        self.assertIn('Accept-Encoding', r.request.headers)
        self.assertIn('gzip', r.request.headers['Accept-Encoding'])

        r = self.api.post("api_manager", {})
        self.assertIn('Accept-Encoding', r.request.headers)
        self.assertIn('gzip', r.request.headers['Accept-Encoding'])

        r = self.api.put("api_manager", {})
        self.assertIn('Accept-Encoding', r.request.headers)
        self.assertIn('gzip', r.request.headers['Accept-Encoding'])

        r = self.api.delete("api_manager")
        self.assertIn('Accept-Encoding', r.request.headers)
        self.assertIn('gzip', r.request.headers['Accept-Encoding'])

    def test_compression_post(self):
        api = APIManager("CLIENT_ID", "CLIENT_SECRET", self.server.path, compression_enabled=True, backoff_config = None)
        content = {
            "some_property": "some_value",
            "some_boolean": True
        }

        r = api.post("compression_enabled", content)

        self.assertIn('Content-Encoding', r.request.headers)
        self.assertEqual('gzip', r.request.headers['Content-Encoding'])

        self.assertIn('Content-Encoding', r.headers)
        self.assertEqual('gzip', r.headers['Content-Encoding'])

        # content already decompressed by python-requests
        self.assertEqual(content, r.json())

    def test_compression_put(self):
        api = APIManager("CLIENT_ID", "CLIENT_SECRET", self.server.path, compression_enabled=True, backoff_config = None)
        content = {
            "some_property": "some_value",
            "some_boolean": True
        }

        r = api.put("compression_enabled", content)

        self.assertIn('Content-Encoding', r.request.headers)
        self.assertEqual('gzip', r.request.headers['Content-Encoding'])

        self.assertIn('Content-Encoding', r.headers)
        self.assertEqual('gzip', r.headers['Content-Encoding'])

        # content already decompressed by python-requests
        self.assertEqual(content, r.json())
