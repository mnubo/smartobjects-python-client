import unittest
import uuid

from ittests.it_test import TestHelper
from smartobjects.model import OwnerAttribute


class TestModelService(unittest.TestCase):
    """
    https://smartobjects.mnubo.com/documentation/api_model.html

    Note:
        this test is only asserting production definitions because sandbox definitions
        can be removed
    """

    @classmethod
    def setUpClass(cls):
        cls.client = TestHelper.getClient()

    def test_export_model(self):
        value = self.client.model.export()

        self.assertTrue(len(value.object_types) > 1)

        self.assertTrue(len(value.event_types) > 2)

        self.assertTrue(len(value.object_attributes) > 1)

        self.assertTrue(len(value.timeseries) > 2)

        self.assertTrue(len(value.owner_attributes) > 1)

        self.assertEqual(len(value.sessionizers), 1)

    def test_timeseries(self):
        tss = self.client.model.get_timeseries()

        self.assertTrue(len(tss) > 3)

    def test_object_attributes(self):
        objs = self.client.model.get_object_attributes()

        self.assertTrue(len(objs) > 2)

    def test_owner_attributes(self):
        owners = self.client.model.get_owner_attributes()

        self.assertTrue(len(owners) > 1)

    def test_event_types(self):
        ets = self.client.model.get_event_types()

        self.assertTrue(len(ets) > 2)
        not_empty = [et for et in ets if et.key == 'event_type1']
        self.assertTrue(len(not_empty[0].timeseries_keys) > 0)

    def test_object_types(self):
        ots = self.client.model.get_object_types()
        self.assertTrue(len(ots) > 1)
        not_empty = [ot for ot in ots if ot.key == 'object_type1']
        self.assertTrue(len(not_empty[0].object_attribute_keys) > 0)

    def test_sandbox_ops(self):
        # we can't reset in it test, all sdk integration tests' use the same namespace
        # self.client.model.sandbox_ops.reset_ops.reset()

        key = str(uuid.uuid4()).replace('-', '')

        self.client.model.sandbox_ops.event_types_ops.createOne({
            'key': key,
            'origin': 'scheduled',
            'description': '',
            'timeseriesKeys': []
        })

        self.client.model.sandbox_ops.event_types_ops.update(key, {
            'key': key,
            'origin': 'unscheduled',
            'description': 'new description',
            'timeseriesKeys': []
        })

        self.client.model.sandbox_ops.object_types_ops.createOne({
            'key': key,
            'description': '',
            'objectAttributesKeys': []
        })

        self.client.model.sandbox_ops.object_types_ops.update(key, {
            'key': key,
            'description': 'new description',
            'timeseriesKeys': []
        })

        ts_key = key + '-ts'
        self.client.model.sandbox_ops.timeseries_ops.createOne({
            'key': ts_key,
            'displayName': '',
            'description': '',
            'type': {
                'highLevelType': 'TEXT'
            },
            'eventTypeKeys': [key]
        })

        self.client.model.sandbox_ops.event_types_ops.add_relation("event_type1", ts_key)
        self.client.model.sandbox_ops.event_types_ops.remove_relation("event_type1", ts_key)

        self.client.model.sandbox_ops.timeseries_ops.update(
            ts_key,
            {
                'displayName': 'new desc',
                'description': 'new dp',
            }
        )

        self.client.model.sandbox_ops.timeseries_ops.deploy(ts_key)

        obj_key = key + '-object'
        self.client.model.sandbox_ops.object_attributes_ops.createOne({
            'key': obj_key,
            'displayName': '',
            'description': '',
            'type': {
                'containerType': 'none',
                'highLevelType': 'AREA'
            },
            'objectTypeKeys': [key]
        })

        self.client.model.sandbox_ops.object_types_ops.add_relation("object_type1", obj_key)
        self.client.model.sandbox_ops.object_types_ops.remove_relation("object_type1", obj_key)

        self.client.model.sandbox_ops.object_attributes_ops.update(
            obj_key,
            {
                'displayName': 'new desc',
                'description': 'new dp',
            }
        )
        self.client.model.sandbox_ops.object_attributes_ops.deploy(obj_key)

        owner_key = key + '-owner'
        owner = OwnerAttribute({
            'key': owner_key,
            'displayName': '',
            'description': '',
            'type': {
                'containerType': 'none',
                'highLevelType': 'FLOAT'
            }
        })
        self.client.model.sandbox_ops.owner_attributes_ops.createOne(owner)

        self.client.model.sandbox_ops.owner_attributes_ops.update(
            owner_key,
            {
                'displayName': 'new desc',
                'description': 'new dp',
            }
        )
        self.client.model.sandbox_ops.owner_attributes_ops.deploy(owner_key)

        self.client.model.sandbox_ops.event_types_ops.delete(key)
        self.client.model.sandbox_ops.object_types_ops.delete(key)
