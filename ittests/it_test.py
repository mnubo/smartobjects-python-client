import unittest
import time
import logging

from smartobjects import SmartObjectsClient
from smartobjects import Environments

import sys
PY3 = sys.version_info[0] >= 3

class TestHelper(object):
    timeout = 240
    delay = 5

    @staticmethod
    def getClient():
        if PY3:
          from configparser import ConfigParser
        else:
          from ConfigParser import ConfigParser

        myconfig = ConfigParser()
        myconfig.read("ittests/creds.ini")
        key = myconfig.get("Credentials", "key")
        secret = myconfig.get("Credentials", "secret")
        return SmartObjectsClient(key, secret, Environments.Sandbox)

    @staticmethod
    def search_event_query(eventId):
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

    @staticmethod
    def search_object_by_owner_query(username):
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

    @staticmethod
    def search_owner_query(username): 
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

    @staticmethod
    def search_object_query(deviceId): 
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

    @staticmethod
    def eventually_assert(myAssert):
        TestHelper.eventually_assert_with_delay(myAssert, TestHelper.timeout, TestHelper.delay)

    @staticmethod
    def eventually_assert_with_delay(myAssert, timeout, delay):
        if (timeout < delay):
            raise ValueError("timeout should be bigger than delay")

        current_time = lambda: int(round(time.time()))

        stopper = current_time() + timeout
        lastAssertException = None

        while current_time() < stopper:
            try:
                myAssert()
                return
            except AssertionError as e:
                lastAssertException = e
                logging.debug("Assert failed: {}. Will retry".format(e))
            except Exception as e:
                raise e
            time.sleep(delay)

        if not lastAssertException:
            logging.debug("Final tentative failed.")
            raise lastAssertException