import unittest

from smartobjects.api_manager import APIManager
from smartobjects.model import *
from smartobjects.model.model import ModelService

from tests.mocks.local_api_server import LocalApiServer


class TestModelService(unittest.TestCase):
    """
    https://smartobjects.mnubo.com/apps/doc/api_model.html
    """

    @classmethod
    def setUpClass(cls):
        cls.server = LocalApiServer()
        cls.server.start()

        cls.api = APIManager("CLIENT_ID", "CLIENT_SECRET", cls.server.path, False)
        cls.model = ModelService(cls.api)

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def test_export_empty(self):
        emptyModelJson = {
          "objectTypes": [],
          "eventTypes": [],
          "ownerAttributes": [],
          "sessionizers": [],
          "orphans": {}
        }
        value = Model(emptyModelJson)
        self.assertEqual(len(value.object_types), 0)
        self.assertEqual(len(value.event_types), 0)
        self.assertEqual(len(value.object_attributes), 0)
        self.assertEqual(len(value.timeseries), 0)
        self.assertEqual(len(value.owner_attributes), 0)
        self.assertEqual(len(value.sessionizers), 0)
        self.assertEqual(len(value.orphans.timeseries), 0)
        self.assertEqual(len(value.orphans.object_attributes), 0)

    def test_export_ok(self):
        value = self.model.export()

        self.assertEqual(len(value.object_types), 1)
        ot = value.object_types[0]
        self.assertEqual(ot.key, "object_type1")
        self.assertEqual(ot.description, "desc")
        self.assertEqual(ot.object_attribute_keys, ["object_text_attribute", "object_int_attribute"])

        self.assertEqual(len(value.event_types), 2)
        et = value.event_types[0]
        self.assertEqual(et.key, "event_type1")
        self.assertEqual(et.description, "desc")
        self.assertEqual(et.origin, "scheduled")
        self.assertEqual(et.timeseries_keys, ["ts_number_attribute", "ts_text_attribute"])
        et2 = value.event_types[1]
        self.assertEqual(et2.key, "event_type2")
        self.assertEqual(et2.description, "desc")
        self.assertEqual(et2.origin, "rule")
        self.assertEqual(et2.timeseries_keys, ["ts_text_attribute"])

        self.assertEqual(len(value.object_attributes), 2)
        obj = value.object_attributes[0]
        self.assertEqual(obj.key, "object_text_attribute")
        self.assertEqual(obj.description, "desc object_text_attribute")
        self.assertEqual(obj.display_name, "dp object_text_attribute")
        self.assertEqual(obj.high_level_type, "TEXT")
        self.assertEqual(obj.container_type, "none")
        obj2 = value.object_attributes[1]
        self.assertEqual(obj2.key, "object_int_attribute")
        self.assertEqual(obj2.description, "desc object_int_attribute")
        self.assertEqual(obj2.display_name, "dp object_int_attribute")
        self.assertEqual(obj2.high_level_type, "INT")
        self.assertEqual(obj2.container_type, "list")

        self.assertEqual(len(value.timeseries), 2)
        ts = value.timeseries[0]
        self.assertEqual(ts.key, "ts_text_attribute")
        self.assertEqual(ts.description, "desc ts_text_attribute")
        self.assertEqual(ts.display_name, "dp ts_text_attribute")
        self.assertEqual(ts.high_level_type, "TEXT")
        ts2 = value.timeseries[1]
        self.assertEqual(ts2.key, "ts_number_attribute")
        self.assertEqual(ts2.description, "desc ts_number_attribute")
        self.assertEqual(ts2.display_name, "dp ts_number_attribute")
        self.assertEqual(ts2.high_level_type, "DOUBLE")

        self.assertEqual(len(value.owner_attributes), 1)
        own = value.owner_attributes[0]
        self.assertEqual(own.key, "owner_text_attribute")
        self.assertEqual(own.description, "desc owner_text_attribute")
        self.assertEqual(own.display_name, "dp owner_text_attribute")
        self.assertEqual(own.high_level_type, "TEXT")
        self.assertEqual(own.container_type, "none")

        self.assertEqual(len(value.sessionizers), 1)
        sess = value.sessionizers[0]
        self.assertEqual(sess.key, "sessionizer")
        self.assertEqual(sess.description, "desc sessionizer")
        self.assertEqual(sess.display_name, "dp sessionizer")
        self.assertEqual(sess.start_event_type_key, "event_type1")
        self.assertEqual(sess.end_event_type_key, "event_type2")

        self.assertEqual(len(value.orphans.timeseries), 1)
        orphan_ts = value.orphans.timeseries[0]
        self.assertEqual(orphan_ts.key, "orphan_ts")
        self.assertEqual(orphan_ts.description, "desc orphan_ts")
        self.assertEqual(orphan_ts.display_name, "dp orphan_ts")
        self.assertEqual(orphan_ts.high_level_type, "ACCELERATION")

        self.assertEqual(len(value.orphans.object_attributes), 1)
        orhpan_obj = value.orphans.object_attributes[0]
        self.assertEqual(orhpan_obj.key, "orphan_object")
        self.assertEqual(orhpan_obj.description, "desc orphan_object")
        self.assertEqual(orhpan_obj.display_name, "dp orphan_object")
        self.assertEqual(orhpan_obj.high_level_type, "EMAIL")
        self.assertEqual(orhpan_obj.container_type, "none")