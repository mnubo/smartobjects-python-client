import unittest
import ConfigParser

from ittests.it_test import TestHelper

class TestModelService(unittest.TestCase):
        """
        https://smartobjects.mnubo.com/apps/doc/api_model.html

        Note: 
            this test is only asserting production definitions because sandbox definitions
            can be removed
        """

        @classmethod
        def setUpClass(cls):
            cls.client = TestHelper.getClient()

        def test_export_model(self):
            value = self.client.model.export()

            self.assertEqual(len(value.object_types), 1)

            self.assertEqual(len(value.event_types), 2)

            self.assertEqual(len(value.object_attributes), 1)

            self.assertEqual(len(value.timeseries), 2)

            self.assertEqual(len(value.owner_attributes), 1)

            self.assertEqual(len(value.sessionizers), 1)
