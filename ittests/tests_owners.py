import unittest
import uuid
import time

from ittests.it_test import TestHelper

class TestOwnersService(unittest.TestCase):
    """
    https://smartobjects.mnubo.com/apps/doc/api_ingestion.html#owners
    """

    @classmethod
    def setUpClass(cls):
      cls.client = TestHelper.getClient()

    def test_delete(self):
      currentUUID = uuid.uuid4()
      usernameToDelete = "usernameToDelete-{}".format(currentUUID)

      with self.assertRaises(ValueError):
        self.client.owners.delete(usernameToDelete)

      self.client.owners.create({
          "username": usernameToDelete,
          "x_password": "password-{}".format(currentUUID),
      })

      def search_owner_created():
          result = self.client.search.search(TestHelper.search_owner_query(usernameToDelete))
          self.assertEqual(len(result), 1)

      self.client.owners.delete(usernameToDelete)

      def search_owner_deleted():
          result = self.client.search.search(TestHelper.search_owner_query(usernameToDelete))
          self.assertEqual(len(result), 0)

    def test_basic_owners(self):
      currentUUID = uuid.uuid4()
      username = "username-{}".format(currentUUID)
      value = "value-{}".format(currentUUID)

      
      self.assertEqual(self.client.owners.owner_exists(username), False)
      self.assertEqual(self.client.owners.owners_exist([username]), {
          username: False
      })

      self.client.owners.create({
          "username": username,
          "x_password": "password-{}".format(currentUUID),
          "owner_text_attribute": value,
      })

      with self.assertRaises(ValueError):
          self.client.owners.create({
            "username": username,
        })

      self.assertEqual(self.client.owners.owner_exists(username), True)
      self.assertEqual(self.client.owners.owners_exist([username]), {
          username: True
      })

      def search_owner_created():
          result = self.client.search.search(TestHelper.search_owner_query(username))
          self.assertEqual(len(result), 1)
          for row in result:
            self.assertEqual(row.get("owner_text_attribute"), value)  

      self.client.owners.update(username, {
          "owner_text_attribute": "newvalue"
      })

      def search_owner_updated():
          result = self.client.search.search(TestHelper.search_owner_query(username))
          self.assertEqual(len(result), 1)
          for row in result:
            self.assertEqual(row.get("owner_text_attribute"), "newvalue")  


    def search_claimed(self, username, deviceId):
      result = self.client.search.search(TestHelper.search_object_by_owner_query(username))
      self.assertEqual(len(result), 1)
      for row in result:
        self.assertEqual(row.get("x_device_id"), deviceId)

    def search_unclaimed(self, username, deviceId):   
      result = self.client.search.search(TestHelper.search_object_by_owner_query(username))
      self.assertEqual(len(result), 1)
      for row in result:
        self.assertEqual(row.get("x_device_id"), deviceId)

    def test_claim_unclaim(self):
      currentUUID = uuid.uuid4()
      username = "username-{}".format(currentUUID)
      deviceId = "deviceId-{}".format(currentUUID)
      self.client.owners.create({
          "username": username,
          "x_password": "password-{}".format(currentUUID),
      })
      self.client.objects.create({
          "x_device_id": deviceId,
          "x_object_type": "object_type1",
      })

      self.client.owners.claim(username, deviceId)

      self.client.owners.unclaim(username, deviceId)

    def test_claim_unclaim_with_body(self):
      currentUUID = uuid.uuid4()
      username = "username-{}".format(currentUUID)
      deviceId = "deviceId-{}".format(currentUUID)
      self.client.owners.create({
          "username": username,
          "x_password": "password-{}".format(currentUUID),
      })
      self.client.objects.create({
          "x_device_id": deviceId,
          "x_object_type": "object_type1",
      })

      self.client.owners.claim(username, deviceId, { "x_timestamp": "2017-04-24T16:13:11+00:00"})

      self.client.owners.unclaim(username, deviceId, { "x_timestamp": "2017-04-24T16:13:11+00:00"})