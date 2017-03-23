import unittest

from smartobjects.api_manager import APIManager
from smartobjects.ingestion.owners import OwnersService

from tests.mocks.local_api_server import LocalApiServer


class TestOwnersService(unittest.TestCase):
    """
    https://sop.mtl.mnubo.com/apps/doc/api.html#owners
    """

    @classmethod
    def setUpClass(cls):
        cls.server = LocalApiServer()
        cls.server.start()

        cls.api = APIManager("CLIENT_ID", "CLIENT_SECRET", cls.server.path, False)
        cls.owners = OwnersService(cls.api)

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def setUp(self):
        self.server.server.backend.clear()

    def test_create_ok(self):
        self.owners.create({
            'username': 'owner_1',
            'color': 'blue'
        })
        self.assertIn('owner_1', self.server.server.backend.owners)

    def test_create_username_missing(self):
        with self.assertRaises(ValueError) as ctx:
            self.owners.create({'location': 'bedroom'})
        self.assertEquals(ctx.exception.message, "username cannot be null or empty.")

    def test_create_username_empty(self):
        with self.assertRaises(ValueError) as ctx:
            self.owners.create({'username': '', 'location': 'bedroom'})
        self.assertEquals(ctx.exception.message, "username cannot be null or empty.")

    def test_claim_ok(self):
        self.server.server.backend.objects['my_device'] = {'x_device_id': 'my_device'}
        self.owners.create({'username': 'owner_1'})

        self.owners.claim('owner_1', 'my_device')

        self.assertEquals(self.server.server.backend.objects['my_device']['x_owner'], 'owner_1')

    def test_claim_username_null(self):
        with self.assertRaises(ValueError) as ctx:
            self.owners.claim(None, "my_device")
        self.assertEquals(ctx.exception.message, "username cannot be null or empty.")

    def test_claim_username_empty(self):
        with self.assertRaises(ValueError) as ctx:
            self.owners.claim("", "my_device")
        self.assertEquals(ctx.exception.message, "username cannot be null or empty.")

    def test_claim_device_id_null(self):
        with self.assertRaises(ValueError) as ctx:
            self.owners.claim("owner_1", None)
        self.assertEquals(ctx.exception.message, "device_id cannot be null or empty.")

    def test_claim_device_id_empty(self):
        with self.assertRaises(ValueError) as ctx:
            self.owners.claim("owner_1", "")
        self.assertEquals(ctx.exception.message, "device_id cannot be null or empty.")

    def test_claim_device_id_not_found(self):
        self.owners.create({'username': 'owner_1'})

        with self.assertRaises(ValueError) as ctx:
            self.owners.claim("owner_1", "my_device")
        self.assertEquals(ctx.exception.message, "Object with x_device_id 'my_device' not found.")

    def test_claim_username_not_found(self):
        self.server.server.backend.objects['my_device'] = {'x_device_id': 'my_device'}

        with self.assertRaises(ValueError) as ctx:
            self.owners.claim("owner_1", "my_device")
        self.assertEquals(ctx.exception.message, "Owner 'owner_1' not found.")

    def test_batch_claim_object_ok(self):
        self.server.server.backend.objects['my_device'] = {'x_device_id': 'my_device'}
        self.server.server.backend.objects['my_device2'] = {'x_device_id': 'my_device2'}
        self.owners.create({'username': 'owner_1'})

        self.owners.batch_claim([{'username': 'owner_1', 'x_device_id': 'my_device'}, {'username': 'owner_1', 'x_device_id': 'my_device2'}])

        self.assertEquals(self.server.server.backend.objects['my_device']['x_owner'], 'owner_1')
        self.assertEquals(self.server.server.backend.objects['my_device2']['x_owner'], 'owner_1')

    def test_batch_claim_list_ok(self):
        self.server.server.backend.objects['my_device'] = {'x_device_id': 'my_device'}
        self.server.server.backend.objects['my_device2'] = {'x_device_id': 'my_device2'}
        self.owners.create({'username': 'owner_1'})

        self.owners.batch_claim([('owner_1', 'my_device'), ('owner_1', 'my_device2')])

        self.assertEquals(self.server.server.backend.objects['my_device']['x_owner'], 'owner_1')
        self.assertEquals(self.server.server.backend.objects['my_device2']['x_owner'], 'owner_1')

    def test_batch_claim_list_owner_not_found(self):
        self.server.server.backend.objects['my_device'] = {'x_device_id': 'my_device'}
        self.server.server.backend.objects['my_device2'] = {'x_device_id': 'my_device2'}
        self.owners.create({'username': 'owner_1'})

        resp = self.owners.batch_claim([('owner_1', 'my_device'), ('owner_2', 'my_device2')])

        self.assertEquals(self.server.server.backend.objects['my_device']['x_owner'], 'owner_1')
        self.assertNotIn('x_owner', self.server.server.backend.objects['my_device2'])

        self.assertEquals(resp[1].result, 'error')
        self.assertEquals(resp[1].id, 'my_device2')
        self.assertEquals(resp[1].message, "Owner 'owner_2' not found.")

    def test_batch_claim_list_device_not_found(self):
        self.server.server.backend.objects['my_device'] = {'x_device_id': 'my_device'}
        self.owners.create({'username': 'owner_1'})

        resp = self.owners.batch_claim([('owner_1', 'my_device'), ('owner_1', 'my_device2')])

        self.assertEquals(self.server.server.backend.objects['my_device']['x_owner'], 'owner_1')
        self.assertNotIn('my_device2', self.server.server.backend.objects)

        self.assertEquals(resp[1].result, 'error')
        self.assertEquals(resp[1].id, 'my_device2')
        self.assertEquals(resp[1].message, "Object with x_device_id 'my_device2' not found.")

    def test_unclaim_ok(self):
        self.server.server.backend.objects['my_device'] = {'x_device_id': 'my_device', 'x_owner': 'owner_1'}
        self.owners.create({'username': 'owner_1'})

        self.owners.unclaim('owner_1', 'my_device')

        self.assertEquals(self.server.server.backend.objects['my_device']['x_owner'], None)

    def test_unclaim_username_null(self):
        with self.assertRaises(ValueError) as ctx:
            self.owners.unclaim(None, "my_device")
        self.assertEquals(ctx.exception.message, "username cannot be null or empty.")

    def test_unclaim_username_empty(self):
        with self.assertRaises(ValueError) as ctx:
            self.owners.unclaim("", "my_device")
        self.assertEquals(ctx.exception.message, "username cannot be null or empty.")

    def test_unclaim_device_id_null(self):
        with self.assertRaises(ValueError) as ctx:
            self.owners.unclaim("owner_1", None)
        self.assertEquals(ctx.exception.message, "device_id cannot be null or empty.")

    def test_unclaim_device_id_empty(self):
        with self.assertRaises(ValueError) as ctx:
            self.owners.unclaim("owner_1", "")
        self.assertEquals(ctx.exception.message, "device_id cannot be null or empty.")

    def test_unclaim_device_id_not_found(self):
        self.owners.create({'username': 'owner_1'})

        with self.assertRaises(ValueError) as ctx:
            self.owners.unclaim("owner_1", "my_device")
        self.assertEquals(ctx.exception.message, "Object with x_device_id 'my_device' not found.")

    def test_unclaim_username_not_found(self):
        self.server.server.backend.objects['my_device'] = {'x_device_id': 'my_device'}

        with self.assertRaises(ValueError) as ctx:
            self.owners.unclaim("owner_1", "my_device")
        self.assertEquals(ctx.exception.message, "Owner 'owner_1' not found.")

    def test_batch_unclaim_object_ok(self):
        self.server.server.backend.objects['my_device'] = {'x_device_id': 'my_device', 'x_owner': 'owner_1'}
        self.server.server.backend.objects['my_device2'] = {'x_device_id': 'my_device2', 'x_owner': 'owner_1'}
        self.owners.create({'username': 'owner_1'})

        self.owners.batch_unclaim([{'username': 'owner_1', 'x_device_id': 'my_device'}, {'username': 'owner_1', 'x_device_id': 'my_device2'}])

        self.assertEquals(self.server.server.backend.objects['my_device']['x_owner'], None)
        self.assertEquals(self.server.server.backend.objects['my_device2']['x_owner'], None)

    def test_batch_unclaim_list_ok(self):
        self.server.server.backend.objects['my_device'] = {'x_device_id': 'my_device', 'x_owner': 'owner_1'}
        self.server.server.backend.objects['my_device2'] = {'x_device_id': 'my_device2', 'x_owner': 'owner_1'}
        self.owners.create({'username': 'owner_1'})

        self.owners.batch_unclaim([('owner_1', 'my_device'), ('owner_1', 'my_device2')])

        self.assertEquals(self.server.server.backend.objects['my_device']['x_owner'], None)
        self.assertEquals(self.server.server.backend.objects['my_device2']['x_owner'], None)

    def test_batch_unclaim_list_owner_not_found(self):
        self.server.server.backend.objects['my_device'] = {'x_device_id': 'my_device', 'x_owner': 'owner_1'}
        self.server.server.backend.objects['my_device2'] = {'x_device_id': 'my_device2'}
        self.owners.create({'username': 'owner_1'})

        resp = self.owners.batch_unclaim([('owner_1', 'my_device'), ('owner_2', 'my_device2')])

        self.assertEquals(self.server.server.backend.objects['my_device']['x_owner'], None)
        self.assertNotIn('x_owner', self.server.server.backend.objects['my_device2'])

        self.assertEquals(resp[1].result, 'error')
        self.assertEquals(resp[1].id, 'my_device2')
        self.assertEquals(resp[1].message, "Owner 'owner_2' not found.")

    def test_batch_unclaim_list_device_not_found(self):
        self.server.server.backend.objects['my_device'] = {'x_device_id': 'my_device', 'x_owner': 'owner_1'}
        self.owners.create({'username': 'owner_1'})

        resp = self.owners.batch_unclaim([('owner_1', 'my_device'), ('owner_1', 'my_device2')])

        self.assertEquals(self.server.server.backend.objects['my_device']['x_owner'], None)
        self.assertNotIn('my_device2', self.server.server.backend.objects)

        self.assertEquals(resp[1].result, 'error')
        self.assertEquals(resp[1].id, 'my_device2')
        self.assertEquals(resp[1].message, "Object with x_device_id 'my_device2' not found.")

    def test_batch_unclaim_list_device_not_claimed(self):
        self.server.server.backend.objects['my_device'] = {'x_device_id': 'my_device'}
        self.owners.create({'username': 'owner_1'})

        resp = self.owners.batch_unclaim([('owner_1', 'my_device')])

        self.assertEquals(resp[0].result, 'error')
        self.assertEquals(resp[0].id, 'my_device')
        self.assertEquals(resp[0].message, "Object with x_device_id 'my_device' is not claimed by 'owner_1'.")

    def test_delete_ok(self):
        self.owners.create({'username': 'owner_1'})
        self.owners.delete('owner_1')
        self.assertNotIn('owner_1', self.server.server.backend.owners)

    def test_delete_username_null(self):
        with self.assertRaises(ValueError) as ctx:
            self.owners.delete(None)
        self.assertEquals(ctx.exception.message, "username cannot be null or empty.")

    def test_delete_username_empty(self):
        with self.assertRaises(ValueError) as ctx:
            self.owners.delete("")
        self.assertEquals(ctx.exception.message, "username cannot be null or empty.")

    def test_delete_not_found(self):
        with self.assertRaises(ValueError) as ctx:
            self.owners.delete("owner_1")
        self.assertEquals(ctx.exception.message, "Owner 'owner_1' not found.")

    def test_update_ok(self):
        self.owners.create({'username': 'owner_1', 'location': 'bedroom'})

        self.owners.update('owner_1', {'some_property': 'blue'})
        self.assertDictContainsSubset({
            'username': 'owner_1',
            'location': 'bedroom',
            'some_property': 'blue'
        }, self.server.server.backend.owners['owner_1'])

    def test_update_username_not_found(self):
        with self.assertRaises(ValueError) as ctx:
            self.owners.update('non_existing', {'some_property': 'blue'})
        self.assertEquals(ctx.exception.message, "Owner 'non_existing' not found.")

    def test_update_username_null(self):
        with self.assertRaises(ValueError) as ctx:
            self.owners.update(None, {})
        self.assertEquals(ctx.exception.message, "username cannot be null or empty.")

    def test_update_username_empty(self):
        with self.assertRaises(ValueError) as ctx:
            self.owners.update("", {})
        self.assertEquals(ctx.exception.message, "username cannot be null or empty.")

    def test_create_update_ok(self):
        self.owners.create({'username': 'owner_1', 'some_property': 'green'})

        self.owners.create_update([
            {'username': 'owner_1', 'some_property': 'blue'},
            {'username': 'owner_2', 'some_property': 'red'}
        ])

        self.assertDictContainsSubset(
            {'username': 'owner_1', 'some_property': 'blue'},
            self.server.server.backend.owners['owner_1']
        )
        self.assertDictContainsSubset(
            {'username': 'owner_2', 'some_property': 'red'},
            self.server.server.backend.owners['owner_2']
        )

    def test_create_update_no_username(self):
        with self.assertRaises(ValueError) as ctx:
            self.owners.create_update([
                {'username': '', 'some_property': 'blue'},
                {'username': 'owner_2', 'some_property': 'red'}
            ])
        self.assertEquals(ctx.exception.message, "username cannot be null or empty.")

    def test_create_update_some_failing(self):
        resp = self.owners.create_update([
            {'username': 'owner_1', 'some_property': 'blue'},
            {'username': 'owner_2', 'some_property': 'red', 'invalid_property': 'rejected by mock backend'}
        ])

        self.assertEquals(resp[0].result, 'success')
        self.assertEquals(resp[0].id, 'owner_1')
        self.assertEquals(resp[1].result, 'error')
        self.assertEquals(resp[1].id, 'owner_2')
        self.assertEquals(resp[1].message, "Unknown field 'invalid_property'")

    def test_owner_exists_ok(self):
        self.owners.create({'username': 'owner_1', 'some_property': 'green'})
        
        self.assertEquals(self.owners.owner_exists('owner_1'), True)
        self.assertEquals(self.owners.owner_exists('non_existing'), False)

    def test_owner_exists_username_null(self):
        with self.assertRaises(ValueError) as ctx:
            self.owners.owner_exists(None)
        self.assertEquals(ctx.exception.message, "username cannot be null or empty.")
        
    def test_owner_exists_username_empty(self):
        with self.assertRaises(ValueError) as ctx:
            self.owners.owner_exists("")
        self.assertEquals(ctx.exception.message, "username cannot be null or empty.")

    def test_owners_exist_ok(self):
        self.owners.create({'username': 'owner_1', 'some_property': 'green'})
        
        resp = self.owners.owners_exist(["owner_1", "non_existing"])

        self.assertEquals(resp, {
            "owner_1": True,
            "non_existing": False
        })

    def test_owners_exist_list_null(self):
        with self.assertRaises(ValueError) as ctx:
            self.owners.owners_exist(None)
        self.assertEquals(ctx.exception.message, "List of username cannot be null or empty.")

