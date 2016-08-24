from mnubo.mnubo_client import MnuboClient
import requests
from requests import Response
from mock import MagicMock


def test_mnubo_client_init():

    response = Response()
    response._content = '{"access_token":"CLIENT_ACCESS_TOKEN","token_type":"Bearer","expires_in":3887999}'
    requests.post = MagicMock(return_value=response)
    mnubo = MnuboClient('CLIENT_ID', 'CLIENT_SECRET', 'HOST')

    assert mnubo
    assert hasattr(mnubo, 'smart_object_services')
    assert hasattr(mnubo, 'event_services')
    assert hasattr(mnubo, 'owner_services')

