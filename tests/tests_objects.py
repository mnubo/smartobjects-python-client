import unittest

from smartobjects.api_manager import APIManager
from smartobjects.ingestion.objects import ObjectsService
from tests.mocks.local_api_server import LocalApiServer


class TestObjectsService(unittest.TestCase):
    """
    https://smartobjects.mnubo.com/documentation/api_ingestion.html#objects
    """

    @classmethod
    def setUpClass(cls):
        cls.server = LocalApiServer()
        cls.server.start()

        cls.api = APIManager("CLIENT_ID", "CLIENT_SECRET", cls.server.path, compression_enabled=False,
                             backoff_config=None, token_override=None)
        cls.objects = ObjectsService(cls.api)

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def setUp(self):
        self.server.server.backend.clear()

    def test_create_ok(self):
        # objects.create doesn't return anything and should not raise any error
        self.objects.create({
            "x_device_id": "vin1234",
            "x_object_type": "car",
            "x_owner": {"username": "foobar@mnubo.com"}
        })
        self.assertIn('vin1234', self.server.server.backend.objects)

    def test_create_array(self):
        with self.assertRaises(ValueError) as ctx:
            self.objects.create([{"x_device_id": "vin12345", "x_object_type": "car"}])
            self.assertEqual(ctx.exception.message, "Expecting a dictionary.")

    def test_create_duplicate(self):
        self.objects.create({"x_device_id": "duplicated_id", "x_object_type": "cow"})
        self.assertIn('duplicated_id', self.server.server.backend.objects)

        with self.assertRaises(ValueError) as ctx:
            self.objects.create({"x_device_id": "duplicated_id", "x_object_type": "cow"})
            self.assertEqual(ctx.exception.message, "Object with device id 'duplicated_id' already exists.")

    def test_create_object_empty(self):
        with self.assertRaises(ValueError) as ctx:
            self.objects.create({})
            self.assertEqual(ctx.exception.message, "Object body cannot be null.")

    def test_create_no_device_id(self):
        with self.assertRaises(ValueError) as ctx:
            self.objects.create({
                "x_object_type": "car",
                "x_owner": {"username": "foobar@mnubo.com"}
            })
            self.assertEqual(ctx.exception.message, "x_device_id cannot be null or empty.")

    def test_create_device_id_null(self):
        with self.assertRaises(ValueError) as ctx:
            self.objects.create({
                "x_device_id": "",
                "x_object_type": "car",
                "x_owner": {"username": "foobar@mnubo.com"}
            })
            self.assertEqual(ctx.exception.message, "x_device_id cannot be null or empty.")

        with self.assertRaises(ValueError) as ctx:
            self.objects.create({
                "x_device_id": None,
                "x_object_type": "car",
                "x_owner": {"username": "foobar@mnubo.com"}
            })
            self.assertEqual(ctx.exception.message, "x_device_id cannot be null or empty.")

    def test_create_no_object_type(self):
        with self.assertRaises(ValueError) as ctx:
            self.objects.create({
                "x_device_id": "vin12345",
                "x_owner": {"username": "foobar@mnubo.com"}
            })
            self.assertEqual(ctx.exception.message, "x_object_type cannot be null or empty.")

    def test_create_object_type_null(self):
        with self.assertRaises(ValueError) as ctx:
            self.objects.create({
                "x_device_id": "vin12345",
                "x_object_type": "",
                "x_owner": {"username": "foobar@mnubo.com"}
            })
            self.assertEqual(ctx.exception.message, "x_object_type cannot be null or empty.")

        with self.assertRaises(ValueError) as ctx:
            self.objects.create({
                "x_device_id": "vin12345",
                "x_object_type": None,
                "x_owner": {"username": "foobar@mnubo.com"}
            })
            self.assertEqual(ctx.exception.message, "x_object_type cannot be null or empty.")

    def test_delete(self):
        self.objects.create({
            "x_device_id": "to_be_deleted",
            "x_object_type": "object",
        })
        self.assertIn('to_be_deleted', self.server.server.backend.objects)

        self.objects.delete("to_be_deleted")
        self.assertNotIn('to_be_deleted', self.server.server.backend.objects)

    def test_delete_no_device_id(self):
        with self.assertRaises(ValueError) as ctx:
            self.objects.delete("")
            self.assertEqual(ctx.exception.message, "x_device_id cannot be null or empty.")

    def test_delete_not_existing(self):
        with self.assertRaises(ValueError) as ctx:
            self.objects.delete("not_existing")
            self.assertEqual(ctx.exception.message, "Object with x_device_id 'not_existing' not found.")

    def test_update(self):
        self.objects.create({
            "x_device_id": "to_be_updated",
            "x_object_type": "object",
            "some_property": "some_value"
        })

        self.objects.update("to_be_updated", {
            "x_owner": {"username": "foobar@mnubo.com"}
        })
        self.assertIn('to_be_updated', self.server.server.backend.objects)
        # not strictly equals since x_registration_date has been added!
        self.assertDictContainsSubset({
            "x_device_id": "to_be_updated",
            "x_object_type": "object",
            "x_owner": {"username": "foobar@mnubo.com"},
            "some_property": "some_value"
        }, self.server.server.backend.objects['to_be_updated'])

    def test_update_not_existing(self):
        with self.assertRaises(ValueError) as ctx:
            self.objects.update("not_existing", {
                "x_owner": {"username": "foobar@mnubo.com"}
            })
            self.assertEqual(ctx.exception.message, "Object with x_device_id 'not_existing' not found.")

    def test_update_no_device_id(self):
        with self.assertRaises(ValueError) as ctx:
            self.objects.update("", {
                "x_owner": {"username": "foobar@mnubo.com"}
            })
            self.assertEqual(ctx.exception.message, "deviceId cannot be null or empty.")

    def test_update_empty_body(self):
        with self.assertRaises(ValueError) as ctx:
            self.objects.update("some_id", {})
            self.assertEqual(ctx.exception.message, "Object body cannot be null or empty.")

    def test_create_batch(self):
        objects = [
            {"x_device_id": "device_1", "x_object_type": "printer", "a_property": "a_value1"},
            {"x_device_id": "device_2", "x_object_type": "printer", "a_property": "a_value2"},
            {"x_device_id": "device_3", "x_object_type": "printer", "a_property": "a_value3"},
        ]
        resp = self.objects.create_update(objects)

        for created, asked in zip(resp, objects):
            self.assertEqual(created.result, 'success')
            self.assertEqual(created.id, asked['x_device_id'])

    def test_create_update(self):
        self.objects.create({"x_device_id": "create_update_2", "x_object_type": "printer"})

        objects = [
            {"x_device_id": "create_update_1", "x_object_type": "printer", "a_property": "a_value1"},
            {"x_device_id": "create_update_2", "a_property": "a_value2"},
            {"x_device_id": "create_update_3", "x_object_type": "printer", "a_property": "a_value3"},
        ]
        resp = self.objects.create_update(objects)

        for created, asked in zip(resp, objects):
            self.assertEqual(created.result, 'success')
            self.assertEqual(created.id, asked['x_device_id'])

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
            self.assertEqual(ctx.exception.message, "x_device_id cannot be null or empty.")

    def test_create_update_some_failing(self):
        """missing x_object_type cannot be validated by the API as it requires knowledge of the model, therefore the
        request is sent and potential errors are to be checked in the returned value"""
        objects = [
            {"x_device_id": "new_device_with_type", "x_object_type": "printer", "a_property": "a_value1"},
            {"x_device_id": "new_device_without_type", "a_property": "a_value2"},
        ]
        resp = self.objects.create_update(objects)

        self.assertEqual(resp[0].result, 'success')
        self.assertEqual(resp[0].id, 'new_device_with_type')
        self.assertEqual(resp[1].result, 'error')
        self.assertEqual(resp[1].id, 'new_device_without_type')
        self.assertEqual(resp[1].message, 'x_object_type cannot be null or empty.')

        self.assertIn('new_device_with_type', self.server.server.backend.objects)
        self.assertNotIn('new_device_without_type', self.server.server.backend.objects)

    def test_exists(self):
        self.objects.create({
            "x_device_id": "existing_device",
            "x_object_type": "object",
        })

        self.assertEqual(self.objects.object_exists("existing_device"), True)
        self.assertEqual(self.objects.object_exists("non_existing"), False)

    def test_exists_device_id_null(self):
        with self.assertRaises(ValueError) as ctx:
            self.objects.object_exists(None)
            self.assertEqual(ctx.exception.message, "deviceId cannot be null or empty.")

    def test_exist_batch(self):
        self.objects.create_update([
            {"x_device_id": "existing_1", "x_object_type": "printer"},
            {"x_device_id": "existing_2", "x_object_type": "cow"},
        ])
        resp = self.objects.objects_exist(["existing_1", "existing_2", "non_existing"])

        self.assertEqual(resp, {
            "existing_1": True,
            "existing_2": True,
            "non_existing": False
        })

    def test_exist_batch_device_id_null(self):
        with self.assertRaises(ValueError) as ctx:
            self.objects.objects_exist(None)
            self.assertEqual(ctx.exception.message, "List of deviceId cannot be null or empty.")


if __name__ == '__main__':
    unittest.main()
