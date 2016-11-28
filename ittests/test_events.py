import unittest
import ConfigParser
import uuid
import time

from ittests.it_test import TestHelper

class TestEventsService(unittest.TestCase):
    """
    https://sop.mtl.mnubo.com/apps/doc/api.html#objects
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
      },{
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

      def searchEvents():
          result = self.client.search.search(TestHelper.searchEventQuery(currentUUID))
          self.assertEqual(len(result), 1)
          for row in result:
            self.assertEqual(row.get("ts_text_attribute"), value)  

          result2 = self.client.search.search(TestHelper.searchEventQuery(currentUUID2))
          self.assertEqual(len(result2), 1)
          for row in result2:
            self.assertEqual(row.get("ts_text_attribute"), value2)  

      TestHelper.eventuallyAssert(searchEvents)