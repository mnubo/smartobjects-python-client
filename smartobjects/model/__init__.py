from typing import List, Dict, Any, ValuesView


class ObjectType(object):
    def __init__(self, *args):
        """ One object type and the bound object attribute keys """
        if len(args) == 1 and isinstance(args[0], dict):
            self._source = args[0]
        else:
            raise ValueError("Invalid arguments")

        self._key = self._source.get('key')
        self._description = self._source.get('description')
        raw_object_attributes = self._source.get('objectAttributes', [])
        self._object_attribute_keys = []
        for rawoa in raw_object_attributes:
            self._object_attribute_keys.append(rawoa.get("key"))

    @classmethod
    def withKeys(cls, source) -> "ObjectType":
        if not isinstance(source, dict):
            raise ValueError("Invalid arguments")
        source['objectAttributes'] = [{'key': objKey} for objKey in source.get('objectAttributesKeys', [])]
        return ObjectType(source)

    @property
    def key(self) -> str:
        """ key of the object type - the key is a unique identifier """
        return self._key

    @property
    def description(self) -> str:
        """ description of the object type """
        return self._description

    @property
    def object_attribute_keys(self) -> list:
        """ keys of all the object attributes bound to the object type """
        return self._object_attribute_keys

    def asJson(self) -> Dict[str, Any]:
        return {
            'key': self.key,
            'description': self.description,
            'objectAttributesKeys': self.object_attribute_keys
        }


class EventType(object):
    def __init__(self, *args):
        """ One event type and the bound timeseries attribute keys """

        if len(args) == 1 and isinstance(args[0], dict):
            self._source = args[0]
        else:
            raise ValueError("Invalid arguments")

        self._key = self._source.get('key')
        self._description = self._source.get('description')
        self._origin = self._source.get('origin')
        raw_timeseries_keys = self._source.get('timeseries', [])
        self._timeseries_keys = []
        for rawts in raw_timeseries_keys:
            self._timeseries_keys.append(rawts.get("key"))

    @classmethod
    def withKeys(cls, source) -> "EventType":
        if not isinstance(source, dict):
            raise ValueError("Invalid arguments")
        source['timeseries'] = [{'key': etKey} for etKey in source.get('timeseriesKeys', [])]
        return EventType(source)

    @property
    def key(self) -> str:
        """ key of the event type - the key is a unique identifier """
        return self._key

    @property
    def description(self) -> str:
        """ description of the event type """
        return self._description

    @property
    def origin(self) -> str:
        """ origin of the event type """
        return self._origin

    @property
    def timeseries_keys(self) -> List[str]:
        """ keys of all the timeseries bound to the event type """
        return self._timeseries_keys

    def asJson(self) -> Dict[str, Any]:
        return {
            'key': self.key,
            'origin': self.origin,
            'description': self.description,
            'timeseriesKeys': self.timeseries_keys
        }


class Timeseries(object):
    def __init__(self, *args):
        """ One timeseries """

        if len(args) == 2 and isinstance(args[0], dict) and isinstance(args[1], list):
            self._source = args[0]
            self._event_type_keys = args[1]
        else:
            raise ValueError("Invalid arguments")

        self._key = self._source.get('key')
        self._display_name = self._source.get('displayName')
        self._description = self._source.get('description')
        self._high_level_type = self._source.get('type').get('highLevelType')

    @property
    def key(self) -> str:
        """ key of the timeseries - the key is a unique identifier """
        return self._key

    @property
    def display_name(self) -> str:
        """ display name of the timeseries """
        return self._display_name

    @property
    def description(self) -> str:
        """ description of the timeseries """
        return self._description

    @property
    def high_level_type(self) -> str:
        """ high level type of the timeseries """
        return self._high_level_type

    @property
    def event_types_keys(self) -> str:
        """ high level type of the timeseries """
        return self._event_type_keys

    def asJson(self) -> Dict[str, Any]:
        return {
            'key': self.key,
            'displayName': self.display_name,
            'description': self.description,
            'type': {
                'highLevelType': self.high_level_type
            },
            'eventTypeKeys': self.event_types_keys
        }


class ObjectAttribute(object):
    def __init__(self, *args):
        """ One object attribute """

        if len(args) == 2 and isinstance(args[0], dict) and isinstance(args[1], list):
            self._source = args[0]
            self._object_type_keys = args[1]
        else:
            raise ValueError("Invalid arguments")

        self._key = self._source.get('key')
        self._display_name = self._source.get('displayName')
        self._description = self._source.get('description')
        self._high_level_type = self._source.get('type').get('highLevelType')
        self._container_type = self._source.get('type').get('containerType')

    @property
    def key(self) -> str:
        """ key of the object attribute - the key is a unique identifier """
        return self._key

    @property
    def display_name(self) -> str:
        """ display name of the object attribute """
        return self._display_name

    @property
    def description(self) -> str:
        """ description of the object attribute """
        return self._description

    @property
    def high_level_type(self) -> str:
        """ high level type of the object attribute """
        return self._high_level_type

    @property
    def container_type(self) -> str:
        """ container type of the object attribute """
        return self._container_type

    @property
    def object_type_keys(self) -> str:
        """ container type of the object attribute """
        return self._object_type_keys

    def asJson(self) -> Dict[str, Any]:
        return {
            'key': self.key,
            'displayName': self.display_name,
            'description': self.description,
            'type': {
                'containerType': self.container_type,
                'highLevelType': self.high_level_type
            },
            'objectTypeKeys': self.object_type_keys
        }


class OwnerAttribute(object):
    def __init__(self, *args):
        """ One owner attribute """

        if len(args) == 1 and isinstance(args[0], dict):
            self._source = args[0]
        else:
            raise ValueError("Invalid arguments")

        self._key = self._source.get('key')
        self._display_name = self._source.get('displayName')
        self._description = self._source.get('description')
        self._high_level_type = self._source.get('type').get('highLevelType')
        self._container_type = self._source.get('type').get('containerType')

    @property
    def key(self) -> str:
        """ key of the owner attribute - the key is a unique identifier """
        return self._key

    @property
    def display_name(self) -> str:
        """ display name of the owner attribute """
        return self._display_name

    @property
    def description(self) -> str:
        """ description of the owner attribute """
        return self._description

    @property
    def high_level_type(self) -> str:
        """ high leve type of the owner attribute """
        return self._high_level_type

    @property
    def container_type(self) -> str:
        """ container type of the owner attribute """
        return self._container_type

    def asJson(self) -> Dict[str, Any]:
        return {
            'key': self.key,
            'displayName': self.display_name,
            'description': self.description,
            'type': {
                'containerType': self.container_type,
                'highLevelType': self.high_level_type
            }
        }


class Sessionizer(object):
    def __init__(self, *args):
        """ One sessionizer """

        if len(args) == 1 and isinstance(args[0], dict):
            self._source = args[0]
        else:
            raise ValueError("Invalid arguments")

        self._key = self._source.get('key')
        self._display_name = self._source.get('displayName')
        self._description = self._source.get('description')
        self._start_event_type_key = self._source.get('startEventTypeKey')
        self._end_event_type_key = self._source.get('endEventTypeKey')

    @property
    def key(self) -> str:
        """ key of the sessionizer - the key is a unique identifier """
        return self._key

    @property
    def display_name(self) -> str:
        """ display name of the sessionizer """
        return self._display_name

    @property
    def description(self) -> str:
        """ description of the sessionizer """
        return self._description

    @property
    def start_event_type_key(self) -> str:
        """ the start event type of the sessionizer """
        return self._start_event_type_key

    @property
    def end_event_type_key(self) -> str:
        """ the end event type of the sessionizer """
        return self._end_event_type_key


class Orphans(object):
    def __init__(self, *args):
        """ Orphan timeseries and object attributes """

        if len(args) == 2 and isinstance(args[0], list) and isinstance(args[1], list):
            self._timeseries = args[0]
            self._object_attributes = args[1]
        else:
            raise ValueError("Invalid arguments")

    @property
    def timeseries(self) -> List[Timeseries]:
        """ array of all the timeseries in the model """
        return self._timeseries

    @property
    def object_attributes(self) -> List[ObjectAttribute]:
        """ array of all the object attributes in the model """
        return self._object_attributes


class Model(object):
    def __init__(self, *args):
        """ Contains the result of a model export """

        if len(args) == 1 and isinstance(args[0], dict):
            self._source = args[0]
        else:
            raise ValueError("Invalid arguments")

        raw_object_types = self._source.get('objectTypes', [])
        self._object_types = []
        self.__all_object_attributes = []
        for rawot in raw_object_types:
            ot = ObjectType(rawot)
            self._object_types.append(ot)
            raw_object_attributes = rawot.get('objectAttributes', [])
            for rawobj in raw_object_attributes:
                obj = ObjectAttribute(rawobj, [ot.key])
                self.__all_object_attributes.append(((obj.key, ot.key), obj))

        obj_by_key = {}
        for k, v in self.__all_object_attributes:
            obj_key = k[0]
            ot_key = k[1]
            exists = obj_by_key.get(obj_key)
            if not exists:
                obj_by_key[obj_key] = v
            else:
                exists._object_type_keys.append(ot_key)

        self._object_attributes = obj_by_key.values()

        raw_event_types = self._source.get('eventTypes', [])
        self._event_types = []
        self.__all_timeseries = []
        for rawet in raw_event_types:
            et = EventType(rawet)
            self._event_types.append(et)
            raw_timeseries = rawet.get('timeseries', [])
            for rawts in raw_timeseries:
                ts = Timeseries(rawts, [et.key])
                self.__all_timeseries.append(((ts.key, et.key), ts))

        ts_by_key = {}
        for k, v in self.__all_timeseries:
            ts_key = k[0]
            et_key = k[1]
            exists = ts_by_key.get(ts_key)
            if not exists:
                ts_by_key[ts_key] = v
            else:
                exists._event_type_keys.append(et_key)

        self._timeseries = ts_by_key.values()

        raw_owner_attributes = self._source.get('ownerAttributes', [])
        self._owner_attributes = []
        for rawown in raw_owner_attributes:
            own = OwnerAttribute(rawown)
            self._owner_attributes.append(own)

        raw_sessionizers = self._source.get('sessionizers', [])
        self._sessionizers = []
        for rawsess in raw_sessionizers:
            sessionizer = Sessionizer(rawsess)
            self._sessionizers.append(sessionizer)

        raw_orphans = self._source.get('orphans')
        self.__orphans_ts = []
        for raw_orphan_ts in raw_orphans.get('timeseries', []):
            ts = Timeseries(raw_orphan_ts, [])
            self.__orphans_ts.append(ts)

        self.__orphans_obj = []
        for raw_orphan_obj in raw_orphans.get('objectAttributes', []):
            obj = ObjectAttribute(raw_orphan_obj, [])
            self.__orphans_obj.append(obj)

        self._orphans = Orphans(self.__orphans_ts, self.__orphans_obj)

    @property
    def raw(self) -> Dict[str, Any]:
        """raw JSON object as returned by the model API"""
        return self._source

    @property
    def object_types(self) -> List[ObjectType]:
        """ array of all the object types in the model """
        return self._object_types

    @property
    def event_types(self) -> List[EventType]:
        """ array of all the event types in the model """
        return self._event_types

    @property
    def object_attributes(self) -> ValuesView[ObjectAttribute]:
        """ array of all the object attributes in the model """
        return self._object_attributes

    @property
    def timeseries(self) -> ValuesView[Timeseries]:
        """ array of all the timeseries in the model """
        return self._timeseries

    @property
    def owner_attributes(self) -> List[OwnerAttribute]:
        """ array of all the owner attributes in the model """
        return self._owner_attributes

    @property
    def sessionizers(self) -> List[Sessionizer]:
        """ array of all the sessionizers in the model """
        return self._sessionizers

    @property
    def orphans(self) -> Orphans:
        """ orphan timeseries and object attributes """
        return self._orphans
