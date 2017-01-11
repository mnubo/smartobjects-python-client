from smart_object import SmartObject
import re


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
    def device_id(self):
        return self._device_id

    @device_id.setter
    def device_id(self, value):
        if value is not None:
            self._device_id = value

    @property
    def event_data(self):
        return self._event_data

    @event_data.setter
    def event_data(self, value):
        if value is None:
            self._event_data = dict()
        if value is not None:
            assert isinstance(value, dict)
        self._event_data = value

    @property
    def event_id(self):
        return self._event_id

    @event_id.setter
    def event_id(self, value):
        self._event_id = value

    @property
    def event_type(self):
        return self._event_type

    @event_type.setter
    def event_type(self, value):
        self._event_type = value

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = value

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        self._latitude = value

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        self._longitude = value

    def build(self):
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
