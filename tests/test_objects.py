import unittest

from mnubo.api_manager import APIManager
from mnubo.ingestion.objects import ObjectsService

from tests.mocks.local_api_server import LocalApiServer


class TestObjectsService(unittest.TestCase):
    """
    https://sop-dev.mtl.mnubo.com/apps/doc/api.html#post-api-v3-objects
    """

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
        # objects.create doesn't return anything and should not raise any error
        self.objects.create({
            "x_device_id": "vin1234",
            "x_object_type": "car",
            "x_owner": {"username": "foobar@mnubo.com"}
        })

    def test_create_duplicate(self):
        self.objects.create({"x_device_id": "duplicated_id", "x_object_type": "cow"})
        with self.assertRaises(ValueError) as ctx:
            self.objects.create({"x_device_id": "duplicated_id", "x_object_type": "cow"})
        self.assertEquals(ctx.exception.message, "Object with device id 'duplicated_id' already exists.")

    def test_create_object_empty(self):
        with self.assertRaises(ValueError) as ctx:
            self.objects.create({})
        self.assertEquals(ctx.exception.message, "Object body cannot be null.")

    def test_create_no_device_id(self):
        with self.assertRaises(ValueError) as ctx:
            self.objects.create({
                "x_object_type": "car",
                "x_owner": {"username": "foobar@mnubo.com"}
            })
        self.assertEquals(ctx.exception.message, "x_device_id cannot be blank.")

    def test_create_device_id_null(self):
        with self.assertRaises(ValueError) as ctx:
            self.objects.create({
                "x_device_id": "",
                "x_object_type": "car",
                "x_owner": {"username": "foobar@mnubo.com"}
            })
        self.assertEquals(ctx.exception.message, "x_device_id cannot be blank.")

        with self.assertRaises(ValueError) as ctx:
            self.objects.create({
                "x_device_id": None,
                "x_object_type": "car",
                "x_owner": {"username": "foobar@mnubo.com"}
            })
        self.assertEquals(ctx.exception.message, "x_device_id cannot be blank.")

    def test_create_no_object_type(self):
        with self.assertRaises(ValueError) as ctx:
            self.objects.create({
                "x_device_id": "vin12345",
                "x_owner": {"username": "foobar@mnubo.com"}
            })
        self.assertEquals(ctx.exception.message, "x_object_type cannot be blank.")

    def test_create_object_type_null(self):
        with self.assertRaises(ValueError) as ctx:
            self.objects.create({
                "x_device_id": "vin12345",
                "x_object_type": "",
                "x_owner": {"username": "foobar@mnubo.com"}
            })
        self.assertEquals(ctx.exception.message, "x_object_type cannot be blank.")

        with self.assertRaises(ValueError) as ctx:
            self.objects.create({
                "x_device_id": "vin12345",
                "x_object_type": None,
                "x_owner": {"username": "foobar@mnubo.com"}
            })
        self.assertEquals(ctx.exception.message, "x_object_type cannot be blank.")

    def test_delete(self):
        self.objects.create({
            "x_device_id": "to_be_deleted",
            "x_object_type": "object",
        })
        self.objects.delete("to_be_deleted")

    def test_delete_no_device_id(self):
        with self.assertRaises(ValueError) as ctx:
            self.objects.delete("")
        self.assertEquals(ctx.exception.message, "x_device_id cannot be blank.")

    def test_delete_not_existing(self):
        with self.assertRaises(ValueError) as ctx:
            self.objects.delete("not_existing")
        self.assertEquals(ctx.exception.message, "Object with x_device_id 'not_existing' not found.")

    def test_update(self):
        self.objects.create({
            "x_device_id": "to_be_updated",
            "x_object_type": "object",
        })

        self.objects.update({
            "x_device_id": "to_be_updated",
            "x_owner":{"username": "foobar@mnubo.com"}
        })

    def test_update_not_existing(self):
        with self.assertRaises(ValueError) as ctx:
            self.objects.update({
                "x_device_id": "not_existing",
                "x_owner": {"username": "foobar@mnubo.com"}
            })
        self.assertEquals(ctx.exception.message, "Object with x_device_id 'not_existing' not found.")

    def test_update_no_device_id(self):
        with self.assertRaises(ValueError) as ctx:
            self.objects.update({
                "x_device_id": "",
                "x_owner": {"username": "foobar@mnubo.com"}
            })
        self.assertEquals(ctx.exception.message, "x_device_id cannot be blank.")

    def test_update_empty_body(self):
        with self.assertRaises(ValueError) as ctx:
            self.objects.update({})
        self.assertEquals(ctx.exception.message, "Object body cannot be null.")

    def test_create_batch(self):
        objects = [
            {"x_device_id": "device_1", "x_object_type": "printer", "a_property": "a_value1"},
            {"x_device_id": "device_2", "x_object_type": "printer", "a_property": "a_value2"},
            {"x_device_id": "device_3", "x_object_type": "printer", "a_property": "a_value3"},
        ]
        resp = self.objects.create_update(objects)

        for created, asked in zip(resp, objects):
            self.assertEquals(created.result, 'success')
            self.assertEquals(created.id, asked['x_device_id'])

    def test_create_update(self):
        self.objects.create({"x_device_id": "create_update_2", "x_object_type": "printer"})

        objects = [
            {"x_device_id": "create_update_1", "x_object_type": "printer", "a_property": "a_value1"},
            {"x_device_id": "create_update_2", "a_property": "a_value2"},
            {"x_device_id": "create_update_3", "x_object_type": "printer", "a_property": "a_value3"},
        ]
        resp = self.objects.create_update(objects)

        for created, asked in zip(resp, objects):
            self.assertEquals(created.result, 'success')
            self.assertEquals(created.id, asked['x_device_id'])

    def test_create_update_no_id(self):
        """x_device_id is required whether we're performing a creation or an updated, therefore it can be validated
        a priori and raises a ValueError
        """
        objects = [
            {"x_device_id": "device_1", "x_object_type": "printer", "a_property": "a_value1"},
            {"x_device_id": "", "x_object_type": "cow", "a_property": "a_value2"}
        ]
        with self.assertRaises(ValueError) as ctx:
            self.objects.create_update(objects)
        self.assertEquals(ctx.exception.message, "x_device_id cannot be blank.")

    def test_create_update_some_failing(self):
        """missing x_object_type cannot be validated by the API as it requires knowledge of the model, therefore the
        request is sent and potential errors are to be checked in the returned value"""
        objects = [
            {"x_device_id": "new_device_with_type", "x_object_type": "printer", "a_property": "a_value1"},
            {"x_device_id": "new_device_without_type", "a_property": "a_value2"},
        ]
        resp = self.objects.create_update(objects)

        self.assertEquals(resp[0].result, 'success')
        self.assertEquals(resp[0].id, 'new_device_with_type')
        self.assertEquals(resp[1].result, 'error')
        self.assertEquals(resp[1].id, 'new_device_without_type')
        self.assertEquals(resp[1].message, 'x_object_type cannot be blank.')

    def test_exists(self):
        self.objects.create({
            "x_device_id": "existing_device",
            "x_object_type": "object",
        })

        self.assertEquals(self.objects.object_exists("existing_device"), True)
        self.assertEquals(self.objects.object_exists("non_existing"), False)

    def test_exists_device_id_null(self):
        with self.assertRaises(ValueError) as ctx:
            self.objects.object_exists(None)
        self.assertEquals(ctx.exception.message, "deviceId cannot be blank.")

    def test_exist_batch(self):
        self.objects.create_update([
            {"x_device_id": "existing_1", "x_object_type": "printer"},
            {"x_device_id": "existing_2", "x_object_type": "cow"},
        ])
        resp = self.objects.objects_exist(["existing_1", "existing_2", "non_existing"])

        self.assertEquals(resp, {
            "existing_1": True,
            "existing_2": True,
            "non_existing": False
        })

    def test_exist_batch_device_id_null(self):
        with self.assertRaises(ValueError) as ctx:
            self.objects.objects_exist(None)
        self.assertEquals(ctx.exception.message, "List of deviceId cannot be blank.")


if __name__ == '__main__':
    unittest.main()