import unittest

from smartobjects.api_manager import APIManager
from smartobjects.restitution import *
from smartobjects.restitution.search import SearchService

from tests.mocks.local_api_server import LocalApiServer


class TestSearchService(unittest.TestCase):
    """
    https://smartobjects.mnubo.com/apps/doc/api_search.html#search-api
    """

    @classmethod
    def setUpClass(cls):
        cls.server = LocalApiServer()
        cls.server.start()

        cls.api = APIManager("CLIENT_ID", "CLIENT_SECRET", cls.server.path, compression_enabled=False, backoff_config = None, token_override=None)
        cls.search = SearchService(cls.api)

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def test_search_ok(self):
        # resultset hard coded from: https://smartobjects.mnubo.com/apps/doc/api_search.html#grouping-by-time-intervals
        resultset = self.search.search({"from": "hardcoded:grouping-by-time-interval"})

        self.assertTrue(isinstance(resultset, ResultSet))

        self.assertEqual(len(resultset), 4)

        for row in resultset:
            self.assertEqual(row.get("COUNT(*)"), 400)
            self.assertEqual(row["COUNT(*)"], 400)
            self.assertEqual(row[1], 400)

            # type conversion
            self.assertEqual(row.get("COUNT(*)", str), "400")
            self.assertEqual(row.get(1, float), 400.0)

            self.assertEqual(row.get("month", lambda date: datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")), datetime(2015, 1, 1, 5))
            self.assertEqual(row.get("month", ResultSet.ToDatetime), datetime(2015, 1, 1, 5))

            # full column as returned by platform
            self.assertEqual(row.raw, ['2015-01-01T05:00:00.000Z', 400])

            # only validating the first row
            break

        self.assertEqual(resultset.get_column_index("COUNT(*)"), 1)
        self.assertEqual(resultset.get_column_type("COUNT(*)"), "long")

        # test invalid access
        with self.assertRaises(IndexError):
            _ = resultset[-1]

        with self.assertRaises(IndexError):
            _ = resultset["funkycats"]

        with self.assertRaises(IndexError):
            resultset[2].get(5)

    def test_search_with_pandas(self):
        resultset = self.search.search({"from": "hardcoded:grouping-by-time-interval"})

        self.assertTrue(isinstance(resultset, ResultSet))

        try:
            import pandas
            self.assertTrue(isinstance(resultset.df, pandas.DataFrame))
        except ImportError:
            self.assertRaises(ImportError)

    def test_search_no_result(self):
        resultset = self.search.search({"from": "empty"})

        self.assertEqual(len(resultset), 0)
        for _ in resultset:
            self.assertTrue(False)

        with self.assertRaises(IndexError):
            _ = resultset[0]

    def test_get_datasets(self):
        datasets = self.search.get_datasets()

        self.assertIsInstance(datasets['owner'], DataSet)
        for dataset in datasets.values():
            self.assertTrue(hasattr(dataset, 'key'))
            self.assertTrue(hasattr(dataset, 'display_name'))
            self.assertTrue(hasattr(dataset, 'fields'))

        self.assertIsInstance(datasets['owner'].fields[0], Field)
        for field in datasets['owner'].fields:
            self.assertTrue(hasattr(field, 'key'))
            self.assertTrue(hasattr(field, 'display_name'))
            self.assertTrue(hasattr(field, 'description'))
            self.assertTrue(hasattr(field, 'high_level_type'))
            self.assertTrue(hasattr(field, 'container_type'))
            self.assertTrue(hasattr(field, 'primary_key'))

        self.assertEqual(datasets['owner'].key, "owner")
        self.assertEqual(datasets['session'].fields[1].description, "The date and time the event have been received by Mnubo")
        self.assertEqual(datasets['session'].fields[1].high_level_type, "DATETIME")

    def test_validate_query_ok(self):
        result = self.search.validate_query({
            "from": "events",
            "limit": 10000,
            "select": [
                {"value": "speed"}
            ]
        })

        self.assertTrue(isinstance(result, QueryValidationResult))
        self.assertEqual(result.is_valid, True)
        self.assertEqual(result.validation_errors, [])

    def test_validate_query_empty(self):
        result = self.search.validate_query({})

        self.assertTrue(isinstance(result, QueryValidationResult))
        self.assertEqual(result.is_valid, False)
        self.assertEqual(result.validation_errors, ["Query cannot be empty or null."])


