import unittest

from smartobjects.api_manager import APIManager
from smartobjects.datalake.datasets import DatalakeService
from tests.mocks.local_api_server import LocalApiServer


class TestDalalakeService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = LocalApiServer()
        cls.server.start()

        cls.api = APIManager("CLIENT_ID", "CLIENT_SECRET", cls.server.path, compression_enabled=False,
                             backoff_config=None, token_override=None)
        cls.datalake = DatalakeService(cls.api)

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def test_dataset_key(self):
        with self.assertRaises(ValueError) as err:
            invalid_dataset_key = ":#$"
            self.datalake._dataset_key_validation(invalid_dataset_key)
        self.assertEqual(err.exception.args[0], f"datasetKey can only contain a-z, A-Z, 0-9, _ and -")
        with self.assertRaises(ValueError) as err:
            invalid_dataset_key = "ea."
            self.datalake._dataset_key_validation(invalid_dataset_key)
        self.assertEqual(err.exception.args[0], f"datasetKey cannot start prefixed product dataset")
        with self.assertRaises(ValueError) as err:
            invalid_dataset_key = "a" * 65
            self.datalake._dataset_key_validation(invalid_dataset_key)
        self.assertEqual(err.exception.args[0], f"datasetKey cannot exceed 64 characters")
        with self.assertRaises(ValueError) as err:
            invalid_dataset_key = None
            self.datalake._dataset_key_validation(invalid_dataset_key)
        self.assertEqual(err.exception.args[0], f"datasetKey can not be None")
        with self.assertRaises(ValueError) as err:
            invalid_dataset_key = ""
            self.datalake._dataset_key_validation(invalid_dataset_key)
        self.assertEqual(err.exception.args[0], f"datasetKey can not be empty")
        with self.assertRaises(ValueError) as err:
            invalid_dataset_key = "x_"
            self.datalake._dataset_key_validation(invalid_dataset_key)
        self.assertEqual(err.exception.args[0],
                         f"datasetKey cannot start with any of the following strings: 'suggested_', 'analyzed_', 'x_','p_', 'sa', 'da_', 'ada_'")
        with self.assertRaises(ValueError) as err:
            invalid_dataset_key = "owner"
            self.datalake._dataset_key_validation(invalid_dataset_key)
        self.assertEqual(err.exception.args[0], f"datasetKey cannot be a system dataset name")

    def test_field_key(self):
        with self.assertRaises(ValueError) as err:
            invalid_field_key = ":#$"
            self.datalake._field_key_validation(invalid_field_key)
        self.assertEqual(err.exception.args[0], f"fieldKey can only contain a-z, A-Z, 0-9, _ and -")
        with self.assertRaises(ValueError) as err:
            invalid_field_key = "a" * 65
            self.datalake._field_key_validation(invalid_field_key)
        self.assertEqual(err.exception.args[0], f"fieldKey cannot exceed 64 characters")
        with self.assertRaises(ValueError) as err:
            invalid_field_key = None
            self.datalake._field_key_validation(invalid_field_key)
        self.assertEqual(err.exception.args[0], f"fieldKey cannot be None")
        with self.assertRaises(ValueError) as err:
            invalid_field_key = ""
            self.datalake._field_key_validation(invalid_field_key)
        self.assertEqual(err.exception.args[0], f"fieldKey cannot be empty")
        with self.assertRaises(ValueError) as err:
            invalid_field_key = "x_"
            self.datalake._field_key_validation(invalid_field_key)
        self.assertEqual(err.exception.args[0], f"fieldKey cannot start with any of the following strings: 'x_'")

    def test_type_key(self):
        with self.assertRaises(ValueError) as err:
            invalid_type_key = None
            self.datalake._type_validation(invalid_type_key)
        self.assertEqual(err.exception.args[0],
                         "Invalid type. Must be in: 'BOOLEAN','INT','LONG','FLOAT','DOUBLE','TEXT','TIME','DATETIME','VOLUME','ACCELERATION','SPEED','STATE','MASS','EMAIL','TEMPERATURE','AREA','LENGTH','COUNTRYISO','SUBDIVISION_1_ISO','SUBDIVISION_2_ISO','TIME_ZONE','DURATION'")
        with self.assertRaises(ValueError) as err:
            invalid_type_key = "string"
            self.datalake._type_validation(invalid_type_key)
        self.assertEqual(err.exception.args[0],
                         "Invalid type. Must be in: 'BOOLEAN','INT','LONG','FLOAT','DOUBLE','TEXT','TIME','DATETIME','VOLUME','ACCELERATION','SPEED','STATE','MASS','EMAIL','TEMPERATURE','AREA','LENGTH','COUNTRYISO','SUBDIVISION_1_ISO','SUBDIVISION_2_ISO','TIME_ZONE','DURATION'")
        with self.assertRaises(ValueError) as err:
            invalid_type_key = "boolean"
            self.datalake._type_validation(invalid_type_key)
        self.assertEqual(err.exception.args[0],
                         "Invalid type. Must be in: 'BOOLEAN','INT','LONG','FLOAT','DOUBLE','TEXT','TIME','DATETIME','VOLUME','ACCELERATION','SPEED','STATE','MASS','EMAIL','TEMPERATURE','AREA','LENGTH','COUNTRYISO','SUBDIVISION_1_ISO','SUBDIVISION_2_ISO','TIME_ZONE','DURATION'")

    def test_dataset_description(self):
        with self.assertRaises(ValueError) as err:
            invalid_dataset_description = "a" * 513
            self.datalake._dataset_description_validation(invalid_dataset_description)
        self.assertEqual(err.exception.args[0], f"dataset description cannot exceed 512 characters")

    def test_dataset_display_name(self):
        with self.assertRaises(ValueError) as err:
            invalid_dataset_display_name = "a" * 256
            self.datalake._dataset_display_name_validation(invalid_dataset_display_name)
        self.assertEqual(err.exception.args[0], f"dataset display name cannot exceed 255 characters")

    def test_field_description(self):
        with self.assertRaises(ValueError) as err:
            invalid_field_description = "a" * 1025
            self.datalake._field_description_validation(invalid_field_description)
        self.assertEqual(err.exception.args[0], f"field description cannot exceed 1024 characters")

    def test_field_display_name(self):
        with self.assertRaises(ValueError) as err:
            invalid_field_display_name = "a" * 256
            self.datalake._field_display_name_validation(invalid_field_display_name)
        self.assertEqual(err.exception.args[0], f"field display name cannot exceed 255 characters")
