import datetime


class MNUOwner(object):
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


class MNUSmartObject(object):
    """A mnubo smart object model with the following properties:

    Properties:
        x_device_id: (string)
        x_object_type: (string)
        x_registration_date: (datetime)
        x_owner: (MNUOwner)
        event_id: (string)
    """

    def __init__(self, device_id=None, object_type=None, registration_date=datetime.datetime.now().isoformat(), owner=None, event_id=None):
        self.x_device_id = device_id
        self.x_object_type = object_type
        self.x_registration_date = registration_date
        self.x_owner = owner
        self.event_id = event_id


class MNUEvent(object):
    """A mnubo event model with the following properties:

    Properties:
        event_id: (string)
        x_object: (MNUSmartObject)
        x_event_type: (string)
        x_timestamp: (datetime)

    """

    def __init__(self, event_id=None, object=None, event_type=None, timestamp=datetime.datetime.now().isoformat(), timeseries=None):
        self.event_id = event_id
        self.x_object = object
        self.x_event_type = event_type
        self.x_timestamp = timestamp
        self.timeseries = timeseries

