import unittest
import uuid

from smartobjects.model import OwnerAttribute
from ittests.it_test import TestHelper

class TestModelService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestHelper.getClient()

    def test_big_data_api(self):
        query = {"from": "event", "select": [{"value": "ts_text_attribute"}], "where": {"ts_text_attribute": {"has": "value"}}}
        start_export = self.client.bigdata.start_export(query)
        self.assertTrue(len(start_export.stream_first_pages) > 0)

        for page in start_export.stream_first_pages:
            streamed = self.client.bigdata.stream_page(page)
            self.assertTrue(len(streamed.rows) > 10)

