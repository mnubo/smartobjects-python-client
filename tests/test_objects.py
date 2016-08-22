import unittest

from mnubo.api_manager import APIManager
from mnubo.ingestion.objects import ObjectsService

from tests.mocks.local_api_server import LocalApiServer


class TestObjectsService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = LocalApiServer()
        cls.server.start()

        cls.api = APIManager("CLIENT_ID", "CLIENT_SECRET", cls.server.path)
        cls.objects = ObjectsService(cls.api)

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def test_create_ok(self):
        """
        https://sop-dev.mtl.mnubo.com/apps/doc/api.html#post-api-v3-objects
        """
        # objects.create doesn't return anything and should not raise any error
        self.objects.create({
            "x_device_id": "vin1234",
            "x_object_type": "car",
            "x_owner": {"username": "foobar@mnubo.com"}
        })

    def test_create_object_null(self):
        raise NotImplementedError

    def test_create_no_device_id(self):
        """
        """
        with self.assertRaises(ValueError) as ctx:
            self.objects.create({
                "x_object_type": "car",
                "x_owner": {"username": "foobar@mnubo.com"}
            })
        self.assertEquals(ctx.exception.message, "x_device_id cannot be blank.")

    def test_create_device_id_null(self):
        raise NotImplementedError

    def test_create_no_object_type(self):
        with self.assertRaises(ValueError) as ctx:
            self.objects.create({
                "x_device_id": "vin12345",
                "x_owner": {"username": "foobar@mnubo.com"}
            })
        self.assertEquals(ctx.exception.message, "x_object_type cannot be blank.")

    def test_create_object_type_null(self):
        raise NotImplementedError

    def test_delete(self):
        raise NotImplementedError

    def test_delete_no_device_id(self):
        raise NotImplementedError

    def test_update(self):
        raise NotImplementedError

    def test_update_no_device_id(self):
        raise NotImplementedError

    def test_update_empty_body(self):
        raise NotImplementedError

    def test_create_update(self):
        raise NotImplementedError

    def test_create_update_one_failing(self):
        raise NotImplementedError

    def test_exists(self):
        raise NotImplementedError

    def test_exists_device_id_null(self):
        raise NotImplementedError

    def test_exist_batch(self):
        raise NotImplementedError

    def test_exist_batch_device_id_null(self):
        raise NotImplementedError