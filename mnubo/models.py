import datetime


class Owner(object):
    """ A mnubo owner object model with the following properties:

    Properties:
        username: (string)
        password: (string)
        registration_date: (datetime)
    """

    def __init__(self, username=None, password=None, registration_date=datetime.datetime.now().isoformat()):
        self.username = username
        self.x_password = password
        self.x_registration_date = registration_date


class Object(object):
    """A mnubo smart object model with the following properties:

    Properties:
        x_device_id: (string)
        x_object_type: (string)
        x_registration_date: (datetime)
        x_owner: (Owner)
    """

    def __init__(self, device_id=None, object_type=None, registration_date=datetime.datetime.now().isoformat(), owner=None):
        self.x_device_id = device_id
        self.x_object_type = object_type
        self.x_registration_date = registration_date
        self.x_owner = owner


class Event(object):
    """ A mnubo event model with the following properties:

    Properties:
        event_id: (string)
        x_object: (Object)
        x_event_type: (string)
        x_timestamp: (datetime)

    """

    def __init__(self, event_id=None, object=None, event_type=None, timestamp=datetime.datetime.now().isoformat(), timeseries=None):
        self.event_id = event_id
        self.x_object = object
        self.x_event_type = event_type
        self.x_timestamp = timestamp
        self.timeseries = timeseries


class AccessToken(object):
    """ An access token model with the following properties

    Properties:
        token: (string)
        expires_in: (int) in seconds
        requested_at: (datetime)
    """

    def __init__(self, token, expires_in, requested_at=datetime.datetime.now()):
        self.token = token
        self.expires_in = datetime.timedelta(seconds=expires_in)
        self.requested_at = requested_at

    def is_valid(self):
        """ Validates if the token is still valid

        :return: True of the token is still valid, False if it is expired
        """

        return self.requested_at + self.expires_in > datetime.datetime.now()