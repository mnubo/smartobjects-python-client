import time
import unittest
import uuid

from requests.exceptions import HTTPError

from ittests.it_test import TestHelper
from smartobjects.datalake.datasets import Dataset, DatasetField, DatasetUpdate, DatasetFieldUpdate


class TestDatalakeService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestHelper.getClient()
        cls.base_key = "python_sdk-"
        cls.field_key = "myvalue"
        cls.base_field = DatasetField(key=cls.field_key, type="BOOLEAN")
        cls.base_dataset = Dataset(key=str(uuid.uuid4()), fields=[cls.base_field])

    def test_create_delete(self):
        schema = self.base_dataset
        test_key = self.base_key + str(uuid.uuid4())
        schema.key = test_key
        with self.assertRaises(HTTPError):
            self.client.datalake.delete(test_key)
        self.client.datalake.create(schema)
        self.client.datalake.delete(test_key)

    def test_list_datasets(self):
        schema = self.base_dataset
        test_key = self.base_key + str(uuid.uuid4())
        schema.key = test_key

        self.client.datalake.create(schema)
        list_of_datasets = self.client.datalake.list()
        list_of_keys = [dataset.key for dataset in list_of_datasets]
        self.assertTrue(test_key in list_of_keys)
        self.client.datalake.delete(test_key)

    def test_get_dataset(self):
        schema = self.base_dataset
        test_key = self.base_key + str(uuid.uuid4())
        schema.key = test_key

        self.client.datalake.create(schema)
        dataset_definition = self.client.datalake.get(test_key)
        self.assertEqual(dataset_definition.key, test_key)
        self.client.datalake.delete(test_key)

    def test_update(self):
        schema = self.base_dataset
        test_key = self.base_key + str(uuid.uuid4())
        schema.key = test_key

        self.client.datalake.create(schema)

        update_schema = DatasetUpdate(displayName="myupdatedschema", description="my updated schema",
                                      metadata={"additionalProp4": "stringupdated"})

        self.client.datalake.update(datasetKey=test_key, dataset=update_schema)

        dataset_definition = self.client.datalake.get(test_key)

        self.assertEqual(dataset_definition.displayName, "myupdatedschema")
        self.assertEqual(dataset_definition.description, "my updated schema")
        self.assertEqual(dataset_definition.metadata, {"additionalProp4": "stringupdated"})

        self.client.datalake.delete(test_key)

    def test_add_field(self):
        schema = self.base_dataset
        test_key = self.base_key + str(uuid.uuid4())
        schema.key = test_key

        self.client.datalake.create(schema)
        new_field = DatasetField(key="new_field", type='BOOLEAN')
        self.client.datalake.add_field(datasetKey=test_key, datasetField=new_field)

        dataset_definition = self.client.datalake.get(test_key)
        fields_list = [field.key for field in dataset_definition.fields]
        self.assertTrue("new_field" in fields_list)
        self.assertFalse("not a new field" in fields_list)

        self.client.datalake.delete(test_key)

    def test_update_field(self):
        schema = self.base_dataset
        test_key = self.base_key + str(uuid.uuid4())
        schema.key = test_key

        self.client.datalake.create(schema)

        field_update = DatasetFieldUpdate(description="updated_string", displayName="updated_string")
        self.client.datalake.update_field(datasetKey=test_key, fieldKey=self.field_key, datasetField=field_update)

        dataset_definition = self.client.datalake.get(test_key)
        fields = dataset_definition.fields
        updated_field = [field for field in fields if field.key == self.field_key][0]
        self.assertEqual(updated_field.description, "updated_string")
        self.assertNotEqual(updated_field.description, "")
        self.assertEqual(updated_field.displayName, "updated_string")
        self.assertNotEqual(updated_field.displayName, "")

        self.client.datalake.delete(test_key)

    def test_send(self):
        schema = self.base_dataset
        test_key = self.base_key + str(uuid.uuid4())
        schema.key = test_key

        self.client.datalake.create(schema)

        data = {self.field_key: True}
        success = False
        error = ""
        time_to_wait = [1, 2, 4, 8, 16, 32, 64, 128]
        for seconds in time_to_wait:
            try:
                self.client.datalake.send(datasetKey=test_key, data=[data])
                success = True
            except Exception as e:
                time.sleep(seconds)
                error = e

        if not success:
            raise Exception(f"Could not ingest data into the dataset because of error: {error}")

        data["unknown-field"] = False
        response = self.client.datalake.send(datasetKey=test_key, data=[data])

        assert response[0]["index"] == 0
        assert response[0]["retryable"] == False