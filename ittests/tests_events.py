import unittest
import uuid

from ittests.it_test import TestHelper


class TestEventsService(unittest.TestCase):
    """
    https://smartobjects.mnubo.com/documentation/api_ingestion.html#events
    """

    @classmethod
    def setUpClass(cls):
        cls.client = TestHelper.getClient()

    def test_basic_events(self):
        currentUUID = "{}".format(uuid.uuid4())
        currentUUID2 = "{}".format(uuid.uuid4())
        value = "value-{}".format(currentUUID)
        value2 = "value-{}".format(currentUUID2)

        self.client.events.send([{
            "event_id": currentUUID,
            "x_object": {
                "x_device_id": "obj"
            },
            "x_event_type": "event_type1",
            "ts_text_attribute": value,
        }, {
            "event_id": currentUUID2,
            "x_object": {
                "x_device_id": "obj"
            },
            "x_event_type": "event_type1",
            "ts_text_attribute": value2,
        }])

        with self.assertRaises(ValueError):
            self.client.events.send({
                "event_id": currentUUID,
                "ts_text_attribute": value,
            })
