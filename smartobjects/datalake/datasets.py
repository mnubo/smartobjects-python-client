import string
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

from typing_extensions import Literal

from smartobjects.api_manager import APIManager


@dataclass
class DatasetField:
    key: str
    type: Literal[
        "BOOLEAN", "INT", "LONG", "FLOAT", "DOUBLE", "TEXT", "TIME", "DATETIME", "VOLUME", "ACCELERATION", "SPEED", "STATE", "MASS", "EMAIL", "TEMPERATURE", "AREA", "LENGTH", "COUNTRYISO", "SUBDIVISION_1_ISO", "SUBDIVISION_2_ISO", "TIME_ZONE", "DURATION"]
    description: Optional[str] = None
    displayName: Optional[str] = None


@dataclass
class DatasetFieldUpdate:
    description: Optional[str] = None
    displayName: Optional[str] = None


@dataclass
class Dataset:
    key: str
    fields: List[DatasetField]
    displayName: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[dict] = field(default_factory=dict)


@dataclass
class DatasetUpdate:
    displayName: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[dict] = None


class DatalakeService(object):
    def __init__(self, api_manager: APIManager):
        """ Initializes DatalakeService with the api manager
        """

        self.api_manager = api_manager
        self.api_version_modeler = "/api/v1"
        self.api_version_ingestion = "/api/v3"

    def _dataset_key_validation(self, datasetKey=str):
        if datasetKey is None:
            raise ValueError(f"datasetKey can not be None")
        if not datasetKey:
            raise ValueError(f"datasetKey can not be empty")
        alphas = string.ascii_uppercase + string.ascii_lowercase + "0123456789" + "-" + "_"
        if datasetKey.startswith(("ea.", "dss.")):
            raise ValueError(f"datasetKey cannot start prefixed product dataset")
        for char in datasetKey:
            if char not in alphas:
                raise ValueError(f"datasetKey can only contain a-z, A-Z, 0-9, _ and -")
        if len(datasetKey) > 64:
            raise ValueError(f"datasetKey cannot exceed 64 characters")
        if datasetKey.lower().startswith(("suggested_", "analyzed_", "x_", "p_", "sa_", "da_", "ada_")):
            raise ValueError(
                f"datasetKey cannot start with any of the following strings: 'suggested_', 'analyzed_', 'x_','p_', 'sa', 'da_', 'ada_'")
        if datasetKey in ["owner", "object", "event", "session", "parametrizeddatasets", "scoring"]:
            raise ValueError(f"datasetKey cannot be a system dataset name")

    def _field_key_validation(self, fieldKey=str):
        if fieldKey is None:
            raise ValueError(f"fieldKey cannot be None")
        if not fieldKey:
            raise ValueError(f"fieldKey cannot be empty")
        alphas = string.ascii_uppercase + string.ascii_lowercase + "0123456789" + "_"
        for char in fieldKey:
            if char not in alphas:
                raise ValueError(f"fieldKey can only contain a-z, A-Z, 0-9 and _")
        if len(fieldKey) > 64:
            raise ValueError(f"fieldKey cannot exceed 64 characters")
        if fieldKey.lower().startswith(("x_")):
            raise ValueError(
                f"fieldKey cannot start with any of the following strings: 'x_'")

    def _dataset_description_validation(self, dataset_description=str):
        if dataset_description:
            if len(dataset_description) > 512:
                raise ValueError(f"dataset description cannot exceed 512 characters")

    def _dataset_display_name_validation(self, display_name=str):
        if display_name:
            if len(display_name) > 255:
                raise ValueError(f"dataset display name cannot exceed 255 characters")

    def _field_description_validation(self, dataset_description=str):
        if dataset_description:
            if len(dataset_description) > 1024:
                raise ValueError(f"field description cannot exceed 1024 characters")

    def _field_display_name_validation(self, display_name=str):
        if display_name:
            if len(display_name) > 255:
                raise ValueError(f"field display name cannot exceed 255 characters")

    def _type_validation(self, high_level_type=Literal[
        "BOOLEAN", "INT", "LONG", "FLOAT", "DOUBLE", "TEXT", "TIME", "DATETIME", "VOLUME", "ACCELERATION", "SPEED", "STATE", "MASS", "EMAIL", "TEMPERATURE", "AREA", "LENGTH", "COUNTRYISO", "SUBDIVISION_1_ISO", "SUBDIVISION_2_ISO", "TIME_ZONE", "DURATION"]):
        if high_level_type not in [
            "BOOLEAN", "INT", "LONG", "FLOAT", "DOUBLE", "TEXT", "TIME", "DATETIME", "VOLUME", "ACCELERATION", "SPEED",
            "STATE", "MASS", "EMAIL", "TEMPERATURE", "AREA", "LENGTH", "COUNTRYISO", "SUBDIVISION_1_ISO",
            "SUBDIVISION_2_ISO", "TIME_ZONE", "DURATION"]:
            raise ValueError(
                f"Invalid type. Must be in: 'BOOLEAN','INT','LONG','FLOAT','DOUBLE','TEXT','TIME','DATETIME','VOLUME','ACCELERATION','SPEED','STATE','MASS','EMAIL','TEMPERATURE','AREA','LENGTH','COUNTRYISO','SUBDIVISION_1_ISO','SUBDIVISION_2_ISO','TIME_ZONE','DURATION'")

    def _field_to_dict(self, field_instance: DatasetField) -> Dict[str, Any]:
        self._field_key_validation(field_instance.key)
        self._type_validation(field_instance.type)
        self._field_display_name_validation(field_instance.displayName)
        self._field_description_validation(field_instance.description)
        field_dict = {
            "key": field_instance.key,
            "type": {
                "highLevelType": field_instance.type
            }
        }

        if field_instance.displayName is not None:
            field_dict["displayName"] = field_instance.displayName
        if field_instance.description is not None:
            field_dict["description"] = field_instance.description
        return field_dict

    def _dataset_to_dict(self, dataset: Dataset) -> Dict[str, Any]:
        self._dataset_key_validation(dataset.key)
        self._dataset_display_name_validation(dataset.displayName)
        self._dataset_description_validation(dataset.description)
        fields_list = [self._field_to_dict(field) for field in dataset.fields]
        dataset_dict = {
            "datasetKey": dataset.key,
            "fields": fields_list,
            "metadata": dataset.metadata
        }
        if dataset.displayName is not None:
            dataset_dict["displayName"] = dataset.displayName
        if dataset.description is not None:
            dataset_dict["description"] = dataset.description
        return dataset_dict

    def _dataset_update_to_dict(self, datasetUpdate: DatasetUpdate) -> Dict[str, Any]:
        update_schema = {
            "metadata": datasetUpdate.metadata
        }
        if datasetUpdate.displayName is not None:
            update_schema["displayName"] = datasetUpdate.displayName
        if datasetUpdate.description is not None:
            update_schema["description"] = datasetUpdate.description
        return update_schema

    def _field_update_to_dict(self, fieldUpdate: DatasetField) -> Dict[str, Any]:
        update_schema = {}
        if fieldUpdate.displayName is not None:
            update_schema["displayName"] = fieldUpdate.displayName
        if fieldUpdate.description is not None:
            update_schema["description"] = fieldUpdate.description
        return update_schema

    def _dict_to_field(self, field_dict: Dict[str, Any]) -> DatasetField:
        field = DatasetField(key=field_dict["key"],
                             type=field_dict["type"],
                             displayName=field_dict["displayName"], description=field_dict["description"])
        return field

    def _dict_to_dataset(self, dataset_dict: Dict[str, Any]) -> Dataset:
        dataset = Dataset(key=dataset_dict["datasetKey"],
                          fields=[self._dict_to_field(field_dict) for field_dict in dataset_dict["fields"]],
                          displayName=dataset_dict["displayName"], description=dataset_dict["description"],
                          metadata=dataset_dict["metadata"])
        return dataset

    def create(self, dataset: Dataset):
        """ Create the streaming dataset
        """
        dataset_dict = self._dataset_to_dict(dataset)
        self.api_manager.post(f"{self.api_version_modeler}/definition/streaming/datasets", dataset_dict)

    def delete(self, datasetKey: str):
        """
        Delete a streaming dataset definition
        """
        if not datasetKey:
            raise ValueError('datasetKey cannot be null or empty.')
        full_path = f"{self.api_version_modeler}/definition/streaming/datasets/{datasetKey}"
        self.api_manager.delete(full_path)

    def list(self) -> List[Dataset]:
        '''
        Get all streaming datasets
        '''

        r = self.api_manager.get(f"{self.api_version_modeler}/definition/streaming/datasets")
        list_json = r.json()
        list_of_datasets = [self._dict_to_dataset(dataset_dict) for dataset_dict in list_json]
        return list_of_datasets

    def update(self, datasetKey: str, dataset: DatasetUpdate):
        '''
        Use this API to update an existing streaming dataset. The body must contain all fields, not only the ones
        that changed. Omitting a field will be interpreted as setting it as NULL. DatasetKey should not be part of the
        body since it is provided in the URL.
        '''
        update_schema = self._dataset_update_to_dict(dataset)
        self.api_manager.put(f"{self.api_version_modeler}/definition/streaming/datasets/{datasetKey}",
                             update_schema)

    def get(self, datasetKey: str) -> Dataset:
        '''
        Get a streaming dataset definition
        '''

        r = self.api_manager.get(f"{self.api_version_modeler}/definition/streaming/datasets/{datasetKey}")
        dataset_dict = r.json()
        dataset = self._dict_to_dataset(dataset_dict)
        return dataset

    def add_field(self, datasetKey: str, datasetField: DatasetField):
        '''
        Add fields to the streaming dataset. For each field, attributes key, and highLevelType are mandatory. The other
        attributes (displayName and description) are optional. Successive calls to this API with different fields will
        append the new fields to the datasets and not replace the existing one.
        '''

        field_dict = self._field_to_dict(datasetField)

        self.api_manager.post(f"{self.api_version_modeler}/definition/streaming/datasets/{datasetKey}/fields",
                              field_dict)

    def update_field(self, datasetKey: str, fieldKey: str, datasetField: DatasetFieldUpdate):
        '''
        Use that API to update a streaming dataset field definition. All properties, can be changed except the key and
        highLevelType. When updating a field, all updatable properties must be specified (displayName, description).
        Otherwise, they will be consider as NULL.
        '''
        field_update = self._field_update_to_dict(datasetField)
        self.api_manager.put(
            f"{self.api_version_modeler}/definition/streaming/datasets/{datasetKey}/fields/{fieldKey}",
            field_update)

    def send(self, datasetKey: str, data: List[Dict[str, Any]]):
        '''
        Use this API to stream data into a dataset.
        '''
        self.api_manager.post(f"{self.api_version_ingestion}/ingestion/datasets/{datasetKey}", data)
