import unittest

from smartobjects.api_manager import APIManager
from smartobjects.bigdata import StartExport, StreamPage
from smartobjects.bigdata.bigdata import BigDataService

from tests.mocks.local_api_server import LocalApiServer

from builtins import filter

class TestBigDataService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = LocalApiServer()
        cls.server.start()

        cls.api = APIManager("CLIENT_ID", "CLIENT_SECRET", cls.server.path, compression_enabled=False, backoff_config = None, token_override=None)
        cls.bigdata = BigDataService(cls.api)

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def test_big_data_api(self):
        query = {"from": "event", "select": [{"value": "ts_text_attribute"}], "where": {"ts_text_attribute": {"has": "value"}}}
        export = self.bigdata.start_export(query)
        self.assertTrue(len(export.stream_first_pages) == 1)

        for page in export.stream_first_pages:
            streamed = self.bigdata.stream_page(page)
            self.assertTrue(len(streamed.rows) == 2)
            self.assertTrue(streamed.rows[0][0] == "one")
            self.assertTrue(streamed.rows[1][0] == "two")
