import unittest
import ConfigParser
import uuid
import time

from ittests.it_test import TestHelper

class TestOwnersService(unittest.TestCase):
    """
    https://sop.mtl.mnubo.com/apps/doc/api.html#owners
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

      def searchOwnerCreated():
          result = self.client.search.search(TestHelper.searchOwnerQuery(usernameToDelete))
          self.assertEqual(len(result), 1)
      TestHelper.eventuallyAssert(searchOwnerCreated)

      self.client.owners.delete(usernameToDelete)

      def searchOwnerDeleted():
          result = self.client.search.search(TestHelper.searchOwnerQuery(usernameToDelete))
          self.assertEqual(len(result), 0)
      TestHelper.eventuallyAssert(searchOwnerDeleted)

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

      def searchOwnerCreated():
          result = self.client.search.search(TestHelper.searchOwnerQuery(username))
          self.assertEqual(len(result), 1)
          for row in result:
            self.assertEqual(row.get("owner_text_attribute"), value)  

      TestHelper.eventuallyAssert(searchOwnerCreated)

      self.client.owners.update(username, {
          "owner_text_attribute": "newvalue"
      })

      def searchOwnerUpdated():
          result = self.client.search.search(TestHelper.searchOwnerQuery(username))
          self.assertEqual(len(result), 1)
          for row in result:
            self.assertEqual(row.get("owner_text_attribute"), "newvalue")  

      TestHelper.eventuallyAssert(searchOwnerUpdated)

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

      def searchClaimed():
          result = self.client.search.search(TestHelper.searchObjectByOwnerQuery(username))
          self.assertEqual(len(result), 1)
          for row in result:
            self.assertEqual(row.get("x_device_id"), deviceId)
      TestHelper.eventuallyAssert(searchClaimed)


      self.client.owners.unclaim(username, deviceId)
      def searchUnclaimed():
          result = self.client.search.search(TestHelper.searchObjectByOwnerQuery(username))
          self.assertEqual(len(result), 1)
          for row in result:
            self.assertEqual(row.get("x_device_id"), deviceId)
      TestHelper.eventuallyAssert(searchUnclaimed)
