import re
from datetime import datetime
from typing import Optional, Dict, Any


class Owner(object):
    def __init__(self):
        """ Initializes everything to None or its base type.
        """
        self._username = None
        self._password = None
        self._last_update_timestamp = None
        self._registration_date = None
        self._registration_latitude = None
        self._registration_longitude = None
        self._timestamp = None
        self._custom_attributes = dict()

    @property
    def custom_attributes(self) -> Dict[str, Any]:
        return self._custom_attributes

    @custom_attributes.setter
    def custom_attributes(self, value):
        if isinstance(value, dict):
            self._custom_attributes = value
        else:
            raise ValueError('Custom attributes must be a dict.')

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, value: Optional[str]):
        if value is not None:
            self._username = value

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, value: Optional[str]):
        if value is not None:
            self._password = value

    @property
    def last_update_timestamp(self) -> datetime:
        return self._last_update_timestamp

    @last_update_timestamp.setter
    def last_update_timestamp(self, value: datetime):
        if value is not None:
            self._last_update_timestamp = value

    @property
    def registration_date(self) -> datetime:
        return self._registration_date

    @registration_date.setter
    def registration_date(self, value: datetime):
        if value is not None:
            self._registration_date = value

    @property
    def registration_latitude(self) -> float:
        return self._registration_latitude

    @registration_latitude.setter
    def registration_latitude(self, value: float):
        if value is not None:
            self._registration_latitude = value

    @property
    def registration_longitude(self) -> float:
        return self._registration_longitude

    @registration_longitude.setter
    def registration_longitude(self, value: float):
        if value is not None:
            self._registration_longitude = value

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value: datetime):
        if value is not None:
            self._timestamp = value

    def build(self) -> Dict[str, Any]:
        """ Builds the owner data structure required by the SmartObjects event ingestion API.
        :return: a dict data structure with the owner data.
        """
        if self.username is None:
            raise ValueError('Cannot create a owner object without at least a username.')

        owner = dict()
        if self.username is not None:
            owner['username'] = self.username

        if self.password is not None:
            owner['x_password'] = self.password

        if self.timestamp is not None:
            owner['x_timestamp'] = self.timestamp

        if self.registration_date is not None:
            owner['x_registration_date'] = self.registration_date

        if self.last_update_timestamp is not None:
            owner['x_last_update_timestamp'] = self.last_update_timestamp

        if self.registration_latitude is not None:
            owner['x_registration_latitude'] = self.registration_latitude

        if self.registration_longitude is not None:
            owner['x_registration_longitude'] = self.registration_longitude

        # We do NOT permit to have any x_ key names since they're reserved.
        p = re.compile(r'x_\w+')
        for k in self._custom_attributes.keys():
            if not p.match(k):
                owner[k] = self._custom_attributes.get(k)

        return owner


class SmartObject(object):
    def __init__(self):
        """ Initializes everything to None or its base type.
        """
        self._object_data = dict()
        self._device_id = None
        self._object_type = None
        self._owner_username = None
        self._timestamp = None
        self._registration_date = None
        self._registration_latitude = None
        self._registration_longitude = None
        self._last_update_timestamp = None
        self._custom_attributes = dict()

    @property
    def device_id(self) -> str:
        return self._device_id

    @device_id.setter
    def device_id(self, value):
        self._device_id = value

    @property
    def object_type(self) -> str:
        return self._object_type

    @object_type.setter
    def object_type(self, value):
        self._object_type = value

    @property
    def owner_username(self) -> str:
        return self._owner_username

    @owner_username.setter
    def owner_username(self, value: str):
        self._owner_username = value

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value: datetime):
        self._timestamp = value

    @property
    def registration_date(self) -> datetime:
        return self._registration_date

    @registration_date.setter
    def registration_date(self, value: datetime):
        self._registration_date = value

    @property
    def registration_latitude(self) -> float:
        return self._registration_latitude

    @registration_latitude.setter
    def registration_latitude(self, value: float):
        self._registration_latitude = value

    @property
    def registration_longitude(self) -> float:
        return self._registration_longitude

    @registration_longitude.setter
    def registration_longitude(self, value: float):
        self._registration_longitude = value

    @property
    def last_update_timestamp(self) -> datetime:
        return self._last_update_timestamp

    @last_update_timestamp.setter
    def last_update_timestamp(self, value: datetime):
        self._last_update_timestamp = value

    @property
    def custom_attributes(self) -> Dict[str, Any]:
        return self._custom_attributes

    @custom_attributes.setter
    def custom_attributes(self, value: Dict[str, Any]):
        if not isinstance(value, dict):
            raise ValueError('Value must be a dictionary.')
        self._custom_attributes = value

    def build(self) -> Dict[str, Any]:
        """ Builds the object data structure required by the SmartObjects event ingestion API.
        :return: a dict data structure with the object data.
        """
        if self.device_id is None:
            raise ValueError('Cannot build SmartObject without a device_id.')

        smart_object = dict()
        if self.device_id is not None:
            smart_object['x_device_id'] = self.device_id
        if self.object_type is not None:
            smart_object['x_object_type'] = self.object_type
        if self.owner_username is not None:
            owner = Owner()
            owner.username = self.owner_username
            smart_object['x_owner'] = owner.build()
        if self.timestamp is not None:
            smart_object['x_timestamp'] = self.timestamp
        if self.registration_date is not None:
            smart_object['x_registration_date'] = self.registration_date
        if self.registration_latitude is not None:
            smart_object['x_registration_latitude'] = self.registration_latitude
        if self.registration_longitude is not None:
            smart_object['x_registration_longitude'] = self.registration_longitude
        if self.last_update_timestamp is not None:
            smart_object['x_last_update_timestamp'] = self.last_update_timestamp

        # We do NOT permit to have any x_ key names since they're reserved.
        p = re.compile(r'x_\w+')
        for k in self.custom_attributes.keys():
            if not p.match(k):
                smart_object[k] = self.custom_attributes.get(k)

        return smart_object


class Event(object):
    def __init__(self):
        """ Initializes everything to None or its base type.
        """
        self._device_id = None
        self._event_data = dict()
        self._event_id = None
        self._event_type = None
        self._latitude = None
        self._longitude = None
        self._timestamp = None

    @property
    def device_id(self) -> str:
        return self._device_id

    @device_id.setter
    def device_id(self, value: str):
        if value is not None:
            self._device_id = value

    @property
    def event_data(self) -> Dict[str, Any]:
        return self._event_data

    @event_data.setter
    def event_data(self, value: Dict[str, Any]):
        if value is None:
            self._event_data = dict()
        if value is not None:
            assert isinstance(value, dict)
        self._event_data = value

    @property
    def event_id(self) -> str:
        return self._event_id

    @event_id.setter
    def event_id(self, value: str):
        self._event_id = value

    @property
    def event_type(self) -> str:
        return self._event_type

    @event_type.setter
    def event_type(self, value: str):
        self._event_type = value

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value: datetime):
        self._timestamp = value

    @property
    def latitude(self) -> float:
        return self._latitude

    @latitude.setter
    def latitude(self, value: float):
        self._latitude = value

    @property
    def longitude(self) -> float:
        return self._longitude

    @longitude.setter
    def longitude(self, value: float):
        self._longitude = value

    def build(self) -> Dict[str, Any]:
        """ Builds the event data structure required by the SmartObjects event ingestion API.
        :return: a dict data structure with the event data.
        """
        event = dict()
        if self.device_id is not None:
            mnubo_object = SmartObject()
            mnubo_object.device_id = self.device_id
            event['x_object'] = mnubo_object.build()

        if self.event_type is not None:
            event['x_event_type'] = self.event_type

        if self.event_id is not None:
            event['event_id'] = self.event_id

        if self.timestamp is not None:
            event['x_timestamp'] = self.timestamp

        if self.latitude is not None:
            event['x_latitude'] = self.latitude

        if self.longitude is not None:
            event['x_longitude'] = self.longitude

        # We do NOT permit to have any x_ key names since they're reserved.
        p = re.compile(r'x_\w+')
        for k in self._event_data.keys():
            if not p.match(k):
                event[k] = self.event_data.get(k)

        return event
