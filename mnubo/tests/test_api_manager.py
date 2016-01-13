from mnubo.api_manager import APIManager
import requests
import datetime
from requests import Response

from mock import MagicMock


def test_api_manager_init():

    response = Response()
    response._content = '{"access_token":"ACCESS_TOKEN","token_type":"Bearer","expires_in":3887999}'
    requests.post = MagicMock(return_value=response)
    auth = APIManager('CLIENT_ID', 'CLIENT_SECRET', 'HOSTNAME')

    requests.post.assert_called_with('HOSTNAME/oauth/token?grant_type=client_credentials', headers={'content-type': 'application/x-www-form-urlencoded', 'Authorization': 'Basic Q0xJRU5UX0lEOkNMSUVOVF9TRUNSRVQ='})

    auth.access_token = auth.fetch_access_token()
    auth_authorization_header = auth.get_token_authorization_header()
    authorization_header = auth.get_authorization_header()
    api_url = auth.get_api_url()
    auth_url = auth.get_auth_url()

    assert auth.access_token['access_token'] == 'ACCESS_TOKEN'
    assert auth.access_token['expires_in'] == datetime.timedelta(seconds=3887999)
    assert auth_authorization_header == {'content-type': 'application/x-www-form-urlencoded', 'Authorization': 'Basic Q0xJRU5UX0lEOkNMSUVOVF9TRUNSRVQ='}
    assert authorization_header == {'content-type': 'application/json', 'Authorization': 'Bearer ACCESS_TOKEN'}
    assert api_url == 'HOSTNAME/api/v3/'
    assert auth_url == 'HOSTNAME/oauth/token?grant_type=client_credentials'


def test_create_operations():

    response = Response()
    response._content = '{"access_token":"ACCESS_TOKEN","token_type":"Bearer","expires_in":3887999}'
    requests.post = MagicMock(return_value=response)

    auth = APIManager('CLIENT_ID', 'CLIENT_SECRET', 'HOSTNAME')

    response = Response()
    response._content = '{"message": "SUCCESS"}'
    requests.post = MagicMock(return_value=response)

    create = auth.post('ROUTE', None)

    assert create == {"message": "SUCCESS"}


def test_put_operation():
    response = Response()
    response._content = '{"access_token":"CLIENT_ACCESS_TOKEN","token_type":"Bearer","expires_in":3887999}'
    requests.post = MagicMock(return_value=response)

    auth = APIManager('CLIENT_ID', 'CLIENT_SECRET', 'HOSTNAME')

    response = Response()
    response._content = '{"message": "SUCCESS"}'
    requests.put = MagicMock(return_value=response)
    put = auth.put('ROUTE', None)
    assert put == {"message": "SUCCESS"}


def test_delete_operation():
    response = Response()
    response._content = '{"access_token":"CLIENT_ACCESS_TOKEN","token_type":"Bearer","expires_in":3887999}'
    requests.post = MagicMock(return_value=response)

    auth = APIManager('CLIENT_ID', 'CLIENT_SECRET', 'HOSTNAME')

    response = Response()
    response._content = '{"message": "SUCCESS"}'
    requests.delete = MagicMock(return_value=response)
    delete = auth.delete('ROUTE')
    assert delete == {"message": "SUCCESS"}


def test_authenticate_decorator():
    response = Response()
    response._content = '{"access_token":"ACCESS_TOKEN","token_type":"Bearer","expires_in":-5}'
    requests.post = MagicMock(return_value=response)

    auth = APIManager('CLIENT_ID', 'CLIENT_SECRET', 'HOSTNAME')

    assert auth.access_token['access_token'] == 'ACCESS_TOKEN'

    response._content = '{"access_token":"REFRESHED_ACCESS_TOKEN","token_type":"Bearer","expires_in":3887999}'
    auth.post('/')

    assert auth.access_token['access_token'] == 'REFRESHED_ACCESS_TOKEN'



