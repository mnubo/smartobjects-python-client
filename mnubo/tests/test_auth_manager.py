from mnubo.api_manager import MNUAPIManager
import requests
import json
from requests import Response

from mock import MagicMock

def test_auth_maneger_init():

    response = Response()
    response._content = '{"access_token":"CLIENT_ACCESS_TOKEN","token_type":"Bearer","expires_in":3887999}'
    requests.post = MagicMock(return_value=response)
    auth = MNUAPIManager('CLIENT_ID', 'CLIENT_SECRET', 'HOSTNAME')

    requests.post.assert_called_with('HOSTNAME/oauth/token?grant_type=client_credentials', headers={'content-type': 'application/x-www-form-urlencoded', 'Authorization': 'Basic Q0xJRU5UX0lEOkNMSUVOVF9TRUNSRVQ='})

    auth.client_access_token = auth.fetch_client_access_token()
    auth_authorization_header = auth.get_token_authorization_header()
    authorization_header = auth.get_authorization_header()
    api_url = auth.get_api_url()
    auth_url = auth.get_auth_url()

    assert auth.client_access_token == 'CLIENT_ACCESS_TOKEN'
    assert auth_authorization_header == {'content-type': 'application/x-www-form-urlencoded', 'Authorization': 'Basic Q0xJRU5UX0lEOkNMSUVOVF9TRUNSRVQ='}
    assert authorization_header == {'content-type': 'application/json', 'Authorization': 'Bearer CLIENT_ACCESS_TOKEN'}
    assert api_url == 'HOSTNAME/api/v3/'
    assert auth_url == 'HOSTNAME/oauth/token?grant_type=client_credentials'


def test_create_operations():

    response = Response()
    response._content = '{"access_token":"CLIENT_ACCESS_TOKEN","token_type":"Bearer","expires_in":3887999}'
    requests.post = MagicMock(return_value=response)

    auth = MNUAPIManager('CLIENT_ID', 'CLIENT_SECRET', 'HOSTNAME')

    response = Response()
    response._content = '{"message": "SUCCESS"}'
    requests.post = MagicMock(return_value=response)

    create = auth.post('ROUTE', None)

    assert create == {"message": "SUCCESS"}


def test_put_operation():
    response = Response()
    response._content = '{"access_token":"CLIENT_ACCESS_TOKEN","token_type":"Bearer","expires_in":3887999}'
    requests.post = MagicMock(return_value=response)

    auth = MNUAPIManager('CLIENT_ID', 'CLIENT_SECRET', 'HOSTNAME')

    response = Response()
    response._content = '{"message": "SUCCESS"}'
    requests.put = MagicMock(return_value=response)
    put = auth.put('ROUTE', None)
    assert put == {"message": "SUCCESS"}

def test_delete_operation():
    response = Response()
    response._content = '{"access_token":"CLIENT_ACCESS_TOKEN","token_type":"Bearer","expires_in":3887999}'
    requests.post = MagicMock(return_value=response)

    auth = MNUAPIManager('CLIENT_ID', 'CLIENT_SECRET', 'HOSTNAME')

    response = Response()
    response._content = '{"message": "SUCCESS"}'
    requests.delete = MagicMock(return_value=response)
    delete = auth.delete('ROUTE')
    assert delete == {"message": "SUCCESS"}