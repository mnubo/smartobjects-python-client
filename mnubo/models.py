import datetime


class Owner(object):
    """A mnubo owner object model with the following properties:

    Properties:
        username: (string)
        password: (string)
        registration_date: (datetime)
    """

    def __init__(self, username=None, password=None, registration_date=datetime.datetime.now().isoformat(), event_id=None):
        self.username = username
        self.x_password = password
        self.x_registration_date = registration_date
        self.event_id = event_id


class Object(object):
    """A mnubo smart object model with the following properties:

    Properties:
        x_device_id: (string)
        x_object_type: (string)
        x_registration_date: (datetime)
        x_owner: (Owner)
        event_id: (string)
    """

    def __init__(self, device_id=None, object_type=None, registration_date=datetime.datetime.now().isoformat(), owner=None, event_id=None):
        self.x_device_id = device_id
        self.x_object_type = object_type
        self.x_registration_date = registration_date
        self.x_owner = owner
        self.event_id = event_id


class Event(object):
    """A mnubo event model with the following properties:

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
    """ Model for access token

    Properties:
        token: (string)
        expiresIn: (int) in seconds
        requestedAt: (datetime)
    """

    def __init__(self, token, expires_in, requested_at=datetime.datetime.now()):
        self.token = token
        self.expires_in = datetime.timedelta(seconds=expires_in)
        self.requested_at = requested_at

    def is_valid(self):
        return self.requested_at + self.expires_in > datetime.datetime.now()