import re


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
    def custom_attributes(self):
        return self._custom_attributes

    @custom_attributes.setter
    def custom_attributes(self, value):
        if isinstance(value, dict):
            self._custom_attributes = value
        else:
            raise ValueError('Custom attributes must be a dict.')

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        if value is not None:
            self._username = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if value is not None:
            self._password = value

    @property
    def last_update_timestamp(self):
        return self._last_update_timestamp

    @last_update_timestamp.setter
    def last_update_timestamp(self, value):
        if value is not None:
            self._last_update_timestamp = value

    @property
    def registration_date(self):
        return self._registration_date

    @registration_date.setter
    def registration_date(self, value):
        if value is not None:
            self._registration_date = value

    @property
    def registration_latitude(self):
        return self._registration_latitude

    @registration_latitude.setter
    def registration_latitude(self, value):
        if value is not None:
            self._registration_latitude = value

    @property
    def registration_longitude(self):
        return self._registration_longitude

    @registration_longitude.setter
    def registration_longitude(self, value):
        if value is not None:
            self._registration_longitude = value

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        if value is not None:
            self._timestamp = value

    def build(self):
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
