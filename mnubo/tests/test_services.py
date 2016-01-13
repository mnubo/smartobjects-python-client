from mnubo.services import OwnerServices, ObjectServices, EventServices
from mock import Mock

####################################
# OwnerServices
####################################


def test_create_owner():
    api_manager_mock = Mock()
    api_manager_mock.post.return_value = 'SUCCESS'

    owner_services = OwnerServices(api_manager_mock)
    owner = {'username': 'USERNAME', 'x_password': 'PASSWORD', 'x_registration_date': '2015-01-01T12:00:00'}

    create = owner_services.create(owner)
    api_manager_mock.post.assert_called_with('owners', {'username': 'USERNAME', 'x_registration_date': '2015-01-01T12:00:00', 'x_password': 'PASSWORD'})
    assert create == 'SUCCESS'


def test_claim_owner():
    api_manager_mock = Mock()
    api_manager_mock.post.return_value = 'SUCCESS'

    owner_services = OwnerServices(api_manager_mock)
    claim = owner_services.claim('owner', 'device_id')

    api_manager_mock.post.assert_called_with('owners/owner/objects/device_id/claim')
    assert claim == 'SUCCESS'


def test_update_owner():
    api_manager_mock = Mock()
    api_manager_mock.put.return_value = 'SUCCESS'

    owner_services = OwnerServices(api_manager_mock)
    owner = {'username': 'USERNAME', 'x_password': 'PASSWORD', 'x_registration_date': '2015-01-01T12:00:00'}
    update = owner_services.update(owner)

    api_manager_mock.put.assert_called_with('owners/USERNAME', {'username': 'USERNAME', 'x_registration_date': '2015-01-01T12:00:00', 'x_password': 'PASSWORD'})
    assert update == 'SUCCESS'


def test_delete_owner():
    api_manager_mock = Mock()
    api_manager_mock.delete.return_value = 'SUCCESS'

    owner_services = OwnerServices(api_manager_mock)
    delete = owner_services.delete('owner')

    api_manager_mock.delete.assert_called_with('owners/owner')
    assert delete == 'SUCCESS'

####################################
# MNUSmartObjectServices
####################################


def test_create_object():
    api_manager_mock = Mock()
    api_manager_mock.post.return_value = 'SUCCESS'

    object_services = ObjectServices(api_manager_mock)
    smart_object = {'x_device_id': 'DEVICE_ID', 'x_object_type': 'OBJECT_TYPE', 'x_registration_date': '2015-01-01T12:00:00'}
    create = object_services.create(smart_object)

    api_manager_mock.post.assert_called_with('objects', {'x_device_id': 'DEVICE_ID', 'x_object_type': 'OBJECT_TYPE', 'x_registration_date': '2015-01-01T12:00:00'})
    assert create == 'SUCCESS'


def test_update_object():
    api_manager_mock = Mock()
    api_manager_mock.put.return_value = 'SUCCESS'

    object_services = ObjectServices(api_manager_mock)
    smart_object = {'x_device_id': 'DEVICE_ID', 'x_object_type': 'OBJECT_TYPE', 'x_registration_date': '2015-01-01T12:00:00'}
    update = object_services.update(smart_object)

    api_manager_mock.put.assert_called_with('objects/DEVICE_ID', {'x_device_id': 'DEVICE_ID', 'x_object_type': 'OBJECT_TYPE', 'x_registration_date': '2015-01-01T12:00:00'})
    assert update == 'SUCCESS'


def test_delete_object():
    api_manager_mock = Mock()
    api_manager_mock.delete.return_value = 'SUCCESS'

    object_services = ObjectServices(api_manager_mock)
    delete = object_services.delete('object')

    api_manager_mock.delete.assert_called_with('objects/object')
    assert delete == 'SUCCESS'

####################################
# EventServices
####################################


def test_send_event():
    api_manager_mock = Mock()
    api_manager_mock.post.return_value = 'SUCCESS'

    event_services = EventServices(api_manager_mock)
    event = {'event_id': 'EVENT_ID', 'x_object': 'OBJECT', 'x_event_type': 'EVENT_TYPE', 'x_timestamp': '2015-11-03T21:40:39.534447'}
    send = event_services.send(event)

    api_manager_mock.post.assert_called_with('events', {'event_id': 'EVENT_ID', 'x_timestamp': '2015-11-03T21:40:39.534447', 'x_event_type': 'EVENT_TYPE', 'x_object': 'OBJECT'})
    assert send == 'SUCCESS'


def test_send_event_to_object():
    pass



