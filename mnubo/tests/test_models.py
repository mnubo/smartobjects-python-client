import datetime

from mnubo.models import Owner
from mnubo.models import Event
from mnubo.models import Object
from mnubo.models import AccessToken


def test_owner_to_dict():
    current_time = datetime.datetime.now().isoformat()
    owner = Owner('USERNAME', 'PASSWORD', current_time, 'EVENT_ID')
    owner.gender = 'male'
    owner.age = 30
    owner.height = 1.80

    owner_dict = owner.__dict__

    assert owner_dict.get('username') == 'USERNAME'
    assert owner_dict.get('x_password') == 'PASSWORD'
    assert owner_dict.get('x_registration_date') == current_time
    assert owner_dict.get('event_id') == 'EVENT_ID'
    assert owner_dict.get('gender') == 'male'
    assert owner_dict.get('age') == 30
    assert owner_dict.get('height') == 1.80


def test_owner_default_values():
    owner = Owner()

    assert owner.username is None
    assert owner.x_password is None
    assert owner.x_registration_date is not None
    assert owner.event_id is None


def test_smart_object_to_dict():
    current_time = datetime.datetime.now().isoformat()
    smart_object = Object('DEVICE_ID', 'OBJECT_TYPE', current_time, None, 'EVENT_ID')

    smart_object_dict = smart_object.__dict__

    assert smart_object_dict.get('x_device_id') == 'DEVICE_ID'
    assert smart_object_dict.get('x_object_type') == 'OBJECT_TYPE'
    assert smart_object_dict.get('x_registration_date') == current_time
    assert smart_object_dict.get('x_owner') is None
    assert smart_object_dict.get('event_id') == 'EVENT_ID'


def test_smart_object_default_values():
    smart_object = Object()

    assert smart_object.x_device_id is None
    assert smart_object.x_object_type is None
    assert smart_object.x_registration_date is not None
    assert smart_object.x_owner is None
    assert smart_object.event_id is None


def test_event_to_dict():
    current_time = datetime.datetime.now().isoformat()
    event = Event('EVENT_ID', None, 'EVENT_TYPE', current_time, None)

    event_dict = event.__dict__

    assert event_dict.get('event_id') == 'EVENT_ID'
    assert event_dict.get('x_object') is None
    assert event_dict.get('x_event_type') == 'EVENT_TYPE'
    assert event_dict.get('x_timestamp') == current_time
    assert event_dict.get('timeseries') is None


def test_event_default_values():
    event = Event()

    assert event.event_id is None
    assert event.x_object is None
    assert event.x_event_type is None
    assert event.x_timestamp is not None
    assert event.timeseries is None


def test_access_token_default_value():
    token = AccessToken('TOKEN', 123)

    assert token.requested_at is not None


def test_access_token_is_valid():
    token = AccessToken('TOKEN', 123, datetime.datetime.now())

    assert token.is_valid() is True


def test_access_token_is_not_valid():
    token = AccessToken('TOKEN', -10, datetime.datetime.now())

    assert token.is_valid() is False
