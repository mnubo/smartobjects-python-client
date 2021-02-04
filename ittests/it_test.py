from smartobjects import Environments
from smartobjects import SmartObjectsClient


class TestHelper(object):
    @staticmethod
    def getClient() -> SmartObjectsClient:
        from configparser import ConfigParser

        myconfig = ConfigParser()
        myconfig.read("ittests/creds.ini")
        key = myconfig.get("Credentials", "key")
        secret = myconfig.get("Credentials", "secret")
        return SmartObjectsClient(key, secret, Environments.Sandbox)


def search_event_query(eventId: str):
    return {
        "from": "event",
        "select": [
            {
                "value": "event_id"
            },
            {
                "value": "ts_text_attribute"
            }
        ],
        "where": {
            "event_id": {
                "eq": eventId.lower()
            }
        }
    }


def search_object_by_owner_query(username: str):
    return {
        "from": "object",
        "select": [
            {
                "value": "x_device_id"
            },
            {
                "value": "object_text_attribute"
            }
        ],
        "where": {
            "x_owner.username": {
                "eq": username.lower()
            }
        }
    }


def search_owner_query(username: str):
    return {
        "from": "owner",
        "select": [
            {
                "value": "username"
            },
            {
                "value": "owner_text_attribute"
            }
        ],
        "where": {
            "username": {
                "eq": username.lower()
            }
        }
    }


def search_object_query(deviceId: str):
    return {
        "from": "object",
        "select": [
            {
                "value": "x_device_id"
            },
            {
                "value": "object_text_attribute"
            }
        ],
        "where": {
            "x_device_id": {
                "eq": deviceId
            }
        }
    }
