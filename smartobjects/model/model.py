from smartobjects.model import Model, Timeseries, ObjectAttribute, OwnerAttribute, EventType, ObjectType


class EntityOps(object):
    def __init__(self, api_manager, cls):
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

    def createOne(self, value):
        """ Creates an entity

        :see create([value])
        """
        self.create([value])

    def create(self, values):
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
                raise ValueError("'values' must contain dict or " + self._class)

        self.api_manager.post("model/{}".format(self._path), payload)

    def update(self, key, update_entity):
        """ Update the entity with the matching key

        update_entity -- json with the following format: {
            'displayName': 'string value',
            'description': 'string value'
        }

        """
        if not isinstance(update_entity, dict):
            raise ValueError("'update_entity' must be dict")

        full_path = "model/{}/{}".format(self._path, key)
        self.api_manager.put(full_path, update_entity)

    def generate_deploy_code(self, key):
        """ Initiate the deploy process of the entity
            with the matching key

        :return code as a string
        """
        full_path = "model/{}/{}/deploy".format(self._path, key)
        json = self.api_manager.post(full_path, None).json()

        if 'code' in json:
            return json.get('code')
        else:
            raise ValueError('Expected a code')

    def apply_deploy_code(self, key, code):
        """ Completes the deploy process of the entity
            with the matching key

        :return code as a string
        """
        full_path = "model/{}/{}/deploy/{}".format(self._path, key, code)
        self.api_manager.post(full_path, None)

    def deploy(self, key):
        """ Runs the complete deploy process of the entity
            with the matching key.
        """
        code = self.generate_deploy_code(key)
        self.apply_deploy_code(key, code)

class TypeOps(object):
    def __init__(self, api_manager, cls):
        """Restricted updates operations specialized for following types:
            - Object Types
            - Event Types
        """
        self._class = cls
        if self._class == EventType:
            self._path = 'eventTypes'
        elif self._class == ObjectType:
            self._path = 'objectTypes'
        else:
            raise ValueError('Supported types are EventType and ObjectType')

        self.api_manager = api_manager

    def createOne(self, value):
        """ Creates a type

        :see create([value])
        """
        self.create([value])

    def create(self, values):
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
                raise ValueError("'values' must contain dict or " + self._class)
        self.api_manager.post("model/{}".format(self._path), payload)

    def update(self, key, value):
        """ Update the type with the matching key
        """
        full_path = "model/{}/{}".format(self._path, key)
        self.api_manager.put(full_path, value)

    def delete(self, key):
        """ Delete the type with the matching key
        """
        full_path = "model/{}/{}".format(self._path, key)
        self.api_manager.delete(full_path)

class ResetOps(object):
    def __init__(self, api_manager):
        """Operations related to the reset process of the sandbox data model
        """
        self.api_manager = api_manager

    def generate_reset_code(self):
        """Initiate the reset process of the sandboxOps data model

        :return code as a string
        """
        json = self.api_manager.post('model/reset', None).json()

        if 'code' in json:
            return json.get('code')
        else:
            raise ValueError('Expected a code')

    def apply_reset_code(self, code):
        """Completes the reset process of the sandboxOps data model
        """
        full_path = "model/reset/{}".format(self._path, code)
        self.api_manager.post(full_path, None)

    def reset(self):
        """Runs the complete reset process of the sandbox data model
        """
        code = self.generate_reset_code()
        self.apply_reset_code(code)



class SandboxOps(object):
    def __init__(self, api_manager):
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
    def timeseries_ops(self):
        """ Sandbox timeseries operations
        :return an instance of EntityOps for timeseries
        """
        return self._ts_ops

    @property
    def object_attributes_ops(self):
        """ Sandbox object attributes operations
        :return an instance of EntityOps for object attributes
        """
        return self._obj_ops

    @property
    def owner_attributes_ops(self):
        """ Sandbox owner attributes operations
        :return an instance of EntityOps for owner attributes
        """
        return self._owner_ops

    @property
    def object_types_ops(self):
        """ Sandbox object types operations
        :return an instance of TypeOps for object types
        """
        return self._ot_ops

    @property
    def event_types_ops(self):
        """ Sandbox event types operations
        :return an instance of TypeOps for event types
        """
        return self._et_ops

    @property
    def reset_ops(self):
        """ Reset the sandbox data model
        :return an instance of ResetOps
        """
        return self._reset_ops


class ModelService(object):
    def __init__(self, api_manager):
        """ Initializes ModelService with the api manager

        see https://smartobjects.mnubo.com/documentation/api_modeler.html for more details
        """

        self.api_manager = api_manager
        self._sandbox_ops = SandboxOps(api_manager)

    @property
    def sandbox_ops(self):
        """ Access to operations only available in the sandbox environment.

        :returns: An instance of SandboxOps
        """
        return self._sandbox_ops

    def export(self):
        """ Export the model in the target environment

        :returns: Model

        Example:
        >>> model = client.model.fetch()
        >>> for obj in value.object_attributes:
        >>>        print(obj.key)
        >>>        print(obj.description)
        """
        return Model(self.api_manager.get('model/export').json())

    def get_timeseries(self):
        """ All timeseries in the target environment.

        :returns: [ObjectAttribute]
        """
        _json = self.api_manager.get('model/timeseries').json()
        return [Timeseries(evt, evt.get('eventTypeKeys', [])) for evt in _json]

    def get_object_attributes(self):
        """ All object attributes in the target environment.

        :returns: [ObjectAttribute]
        """
        _json = self.api_manager.get('model/objectAttributes').json()
        return [ObjectAttribute(evt, evt.get('objectTypeKeys', [])) for evt in _json]

    def get_owner_attributes(self):
        """ All owner attributes in the target environment.

        :returns: [OwnerAttribute]
        """
        _json = self.api_manager.get('model/ownerAttributes').json()
        return [OwnerAttribute(evt) for evt in _json]

    def get_object_types(self):
        """ All object types in the target environment.

        :returns: [ObjectType]
        """
        _json = self.api_manager.get('model/objectTypes').json()
        return [ObjectType.withKeys(evt) for evt in _json]

    def get_event_types(self):
        """ All event types in the target environment.

        :returns: [EventType]
        """
        _json = self.api_manager.get('model/eventTypes').json()
        return [EventType.withKeys(evt) for evt in _json]