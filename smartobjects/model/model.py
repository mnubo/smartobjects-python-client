from typing import Union, Dict, Any, List, Type

from smartobjects.api_manager import APIManager
from smartobjects.model import Model, Timeseries, ObjectAttribute, OwnerAttribute, EventType, ObjectType


class EntityOps(object):
    def __init__(self, api_manager: APIManager,
                 cls: Union[Type[Timeseries], Type[ObjectAttribute], Type[OwnerAttribute]]):
        """Restricted updates operations specialized for the following entities:
            - Object Attribute
            - Owner Attribute
            - Timeseries
        """
        self._class = cls
        if self._class == Timeseries:
            self._path = 'timeseries'
        elif self._class == ObjectAttribute:
            self._path = 'objectAttributes'
        elif self._class == OwnerAttribute:
            self._path = 'ownerAttributes'
        else:
            raise ValueError('Supported entities are Timeseries, ObjectAttribute and OwnerAttribute')

        self.api_manager = api_manager
        self.api_version = "/api/v3"

    def createOne(self, value: Dict[str, Any]):
        """ Creates an entity

        :see create([value])
        """
        self.create([value])

    def create(self, values: List[Union[Timeseries, OwnerAttribute, Dict[str, Any]]]):
        """ Creates multiple entities

        values -- an array of dict or object matching self._class
                  self._class can be Timeseries, OwnerAttribute and
                  ObjectAttribute

        """
        if not isinstance(values, list):
            raise ValueError("'values' must be a list")

        payload = []
        for v in values:
            if isinstance(v, dict):
                payload.append(v)
            elif isinstance(v, self._class):
                payload.append(v.asJson())
            else:
                raise ValueError("'values' must contain dict or " + str(self._class))

        self.api_manager.post(f"{self.api_version}/model/{self._path}", payload)

    def update(self, key: str, update_entity: Dict[str, str]):
        """ Update the entity with the matching key

        update_entity -- json with the following format: {
            'displayName': 'string value',
            'description': 'string value'
        }

        """
        if not isinstance(update_entity, dict):
            raise ValueError("'update_entity' must be dict")

        full_path = f"{self.api_version}/model/{self._path}/{key}"
        self.api_manager.put(full_path, update_entity)

    def generate_deploy_code(self, key: str) -> str:
        """ Initiate the deploy process of the entity
            with the matching key

        :return code as a string
        """
        full_path = f"{self.api_version}/model/{self._path}/{key}/deploy"
        json = self.api_manager.post(full_path, None).json()

        if 'code' in json:
            return json.get('code')
        else:
            raise ValueError('Expected a code')

    def apply_deploy_code(self, key: str, code: str):
        """ Completes the deploy process of the entity
            with the matching key

        :return code as a string
        """
        full_path = f"{self.api_version}/model/{self._path}/{key}/deploy/{code}"
        self.api_manager.post(full_path, None)

    def deploy(self, key: str):
        """ Runs the complete deploy process of the entity
            with the matching key.
        """
        code = self.generate_deploy_code(key)
        self.apply_deploy_code(key, code)


class TypeOps(object):
    def __init__(self, api_manager: APIManager, cls: Union[Type[EventType], Type[ObjectType]]):
        """Restricted updates operations specialized for following types:
            - Object Types
            - Event Types
        """
        self._class = cls
        if self._class == EventType:
            self._path = 'eventTypes'
            self._entity_path = 'timeseries'
        elif self._class == ObjectType:
            self._path = 'objectTypes'
            self._entity_path = 'objectAttributes'
        else:
            raise ValueError('Supported types are EventType and ObjectType')

        self.api_manager = api_manager

        self.api_version = "/api/v3"

    def createOne(self, value: Dict[str, Any]):
        """ Creates a type

        :see create([value])
        """
        self.create([value])

    def create(self, values: List[Union[EventType, ObjectType, Dict[str, Any]]]):
        """ Creates multiple types

        values -- an array of dict or object matching self._class
                  self._class can be EventType or ObjectType

        """
        if not isinstance(values, list):
            raise ValueError("'values' must be a list")

        payload = []
        for v in values:
            if isinstance(v, dict):
                payload.append(v)
            elif isinstance(v, self._class):
                payload.append(v.asJson())
            else:
                raise ValueError("'values' must contain dict or " + str(self._class))
        self.api_manager.post(f"{self.api_version}/model/{self._path}", payload)

    def update(self, key: str, value: dict):
        """ Update the type with the matching key
        """
        full_path = f"{self.api_version}/model/{self._path}/{key}"
        self.api_manager.put(full_path, value)

    def delete(self, key: str):
        """ Delete the type with the matching key
        """
        full_path = f"{self.api_version}/model/{self._path}/{key}"
        self.api_manager.delete(full_path)

    def add_relation(self, key: str, entity_key: str):
        """ Add a relation from the type identified by `key` to
            the entity identified by `entity_key`
        """
        full_path = f"{self.api_version}/model/{self._path}/{key}/{self._entity_path}/{entity_key}"
        self.api_manager.post(full_path)

    def remove_relation(self, key: str, entity_key: str):
        """ Remove a relation from the type identified by `typeKey` to
            the entity identified by `entityKey`
        """
        full_path = f"{self.api_version}/model/{self._path}/{key}/{self._entity_path}/{entity_key}"
        self.api_manager.delete(full_path)


class ResetOps(object):
    def __init__(self, api_manager: APIManager):
        """Operations related to the reset process of the sandbox data model
        """
        self.api_manager = api_manager
        self.api_version = "/api/v3/"

    def generate_reset_code(self):
        """Initiate the reset process of the sandboxOps data model

        :return code as a string
        """
        json = self.api_manager.post(f'{self.api_version}/model/reset', None).json()

        if 'code' in json:
            return json.get('code')
        else:
            raise ValueError('Expected a code')

    def apply_reset_code(self, code: str):
        """Completes the reset process of the sandboxOps data model
        """
        full_path = f"{self.api_version}/model/reset/{code}"
        self.api_manager.post(full_path, None)

    def reset(self):
        """Runs the complete reset process of the sandbox data model
        """
        code = self.generate_reset_code()
        self.apply_reset_code(code)


class SandboxOps(object):
    def __init__(self, api_manager: APIManager):
        """
         Updates operations are only available in sandbox. If you call methods on this interface when your
         client is configured to hit the production environment, you'll get undefined behaviour:
          - 404 Not Found
          - Bad Request
          - etc.
        """
        self.api_manager = api_manager
        self._ts_ops = EntityOps(api_manager, Timeseries)
        self._obj_ops = EntityOps(api_manager, ObjectAttribute)
        self._owner_ops = EntityOps(api_manager, OwnerAttribute)

        self._et_ops = TypeOps(api_manager, EventType)
        self._ot_ops = TypeOps(api_manager, ObjectType)

        self._reset_ops = ResetOps(api_manager)

    @property
    def timeseries_ops(self) -> EntityOps:
        """ Sandbox timeseries operations
        :return an instance of EntityOps for timeseries
        """
        return self._ts_ops

    @property
    def object_attributes_ops(self) -> EntityOps:
        """ Sandbox object attributes operations
        :return an instance of EntityOps for object attributes
        """
        return self._obj_ops

    @property
    def owner_attributes_ops(self) -> EntityOps:
        """ Sandbox owner attributes operations
        :return an instance of EntityOps for owner attributes
        """
        return self._owner_ops

    @property
    def object_types_ops(self) -> TypeOps:
        """ Sandbox object types operations
        :return an instance of TypeOps for object types
        """
        return self._ot_ops

    @property
    def event_types_ops(self) -> TypeOps:
        """ Sandbox event types operations
        :return an instance of TypeOps for event types
        """
        return self._et_ops

    @property
    def reset_ops(self) -> ResetOps:
        """ Reset the sandbox data model
        :return an instance of ResetOps
        """
        return self._reset_ops


class ModelService(object):
    def __init__(self, api_manager: APIManager):
        """ Initializes ModelService with the api manager

        see https://smartobjects.mnubo.com/documentation/api_modeler.html for more details
        """

        self.api_manager = api_manager
        self._sandbox_ops = SandboxOps(api_manager)
        self.api_version = "/api/v3"

    @property
    def sandbox_ops(self) -> SandboxOps:
        """ Access to operations only available in the sandbox environment.

        :returns: An instance of SandboxOps
        """
        return self._sandbox_ops

    def export(self) -> Model:
        """ Export the model in the target environment

        :returns: Model

        Example:
        >>> model = client.model.fetch()
        >>> for obj in value.object_attributes:
        >>>        print(obj.key)
        >>>        print(obj.description)
        """
        return Model(self.api_manager.get(f'{self.api_version}/model/export').json())

    def get_timeseries(self) -> List[Timeseries]:
        """ All timeseries in the target environment.

        :returns: [Timeseries]
        """
        _json = self.api_manager.get(f'{self.api_version}/model/timeseries').json()
        return [Timeseries(evt, evt.get('eventTypeKeys', [])) for evt in _json]

    def get_object_attributes(self) -> List[ObjectAttribute]:
        """ All object attributes in the target environment.

        :returns: [ObjectAttribute]
        """
        _json = self.api_manager.get(f'{self.api_version}/model/objectAttributes').json()
        return [ObjectAttribute(evt, evt.get('objectTypeKeys', [])) for evt in _json]

    def get_owner_attributes(self) -> List[OwnerAttribute]:
        """ All owner attributes in the target environment.

        :returns: [OwnerAttribute]
        """
        _json = self.api_manager.get(f'{self.api_version}/model/ownerAttributes').json()
        return [OwnerAttribute(evt) for evt in _json]

    def get_object_types(self) -> List[ObjectType]:
        """ All object types in the target environment.

        :returns: [ObjectType]
        """
        _json = self.api_manager.get(f'{self.api_version}/model/objectTypes').json()
        return [ObjectType.withKeys(evt) for evt in _json]

    def get_event_types(self) -> List[EventType]:
        """ All event types in the target environment.

        :returns: [EventType]
        """
        _json = self.api_manager.get(f'{self.api_version}/model/eventTypes').json()
        return [EventType.withKeys(evt) for evt in _json]
