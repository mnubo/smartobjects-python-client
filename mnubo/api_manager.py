import requests
import json
import base64

class MNUAPIManager(object):

    def __init__(self, client_id, client_secret, hostname):
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__hostname = hostname
        self.client_access_token = self.fetch_client_access_token()

    def fetch_client_access_token(self):
    	r = requests.post(self.get_auth_url(), headers=self.get_token_authorization_header())
    	jsonResponse = json.loads(r.content)
    	return jsonResponse['access_token']

    def get_token_authorization_header(self):
        return {'content-type': 'application/x-www-form-urlencoded', 'Authorization': "Basic " + base64.b64encode(self.__client_id + ":" + self.__client_secret)}

    def get_authorization_header(self):
        return {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.client_access_token}

    def get_api_url(self):
        return self.__hostname + '/api/v3/'

    def get_auth_url(self):
        return self.__hostname + '/oauth/token?grant_type=client_credentials'

    def post(self, route, body={}):
        url = self.get_api_url() + route
        headers = self.get_authorization_header()
        r = requests.post(url, json=body, headers=headers)
        return json.loads(r.content)

    def put(self, route, body={}):
        url = self.get_api_url() + route
        headers = self.get_authorization_header()
        r = requests.put(url, json=body, headers=headers)
        return json.loads(r.content)

    def delete(self, route):
        url = self.get_api_url() + route
        headers = self.get_authorization_header()
        r = requests.delete(url, headers=headers)
        return json.loads(r.content)
