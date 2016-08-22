import uuid
from datetime import datetime

from routes import route


class MockMnuboBackend(object):
    def __init__(self):
        self.clear()

    def clear(self):
        self.events = {}
        self.owners = {}
        self.objects = {}

    @route('POST', '^/oauth/.*')
    def auth(self, body, params):
        return 200, {
            "access_token": "<TOKEN>",
            "token_type": "Bearer",
            "expires_in": 3600,
            "scope": "ALL",
            "jti": str(uuid.uuid4())
        }

    # events
    def _process_event(self, event, must_exists, by_dev_id=None):
        if "x_object" not in event and "x_device_id" not in event["x_object"]:
            return {"result": "error", "message": "Missing x_object.x_device_id"}

        if "x_event_type" not in event:
            return {"result": "error", "message": "Missing x_event_type"}

        if by_dev_id:
            if 'x_object' in event and 'x_device_id' in event['x_object'] and event["x_object"]["x_device_id"] != by_dev_id:
                return {"result": "error", "message": NotImplemented}
            device_id = by_dev_id
        else:
            device_id = event["x_object"]["x_device_id"]

        if must_exists and device_id not in self.objects:
            return {"result": "error", "message": "Object '{0}' not found".format(device_id)}

        id = uuid.uuid4()
        self.events[id] = event

        return {"result": "success", "id": id, "objectExists": device_id in self.objects}

    @route('POST', r'^/events(?:\?([a-z=_]+)?)?(?:&([a-z=_]+)?)?$')
    def post_events(self, body, params):
        must_exists, report_result = False, False
        for p in params:
            if p and p.startswith('must_exist'):
                must_exists = p.endswith('true')
            if p and p.startswith('report_result'):
                report_result = p.endswith('true')

        result = [self._process_event(event, must_exists) for event in body]
        failed = filter(lambda r: r['result'] != "success", result)

        if report_result:
            return 207 if failed else 200, result
        else:
            if failed:
                return 400, failed[0]['message']
            else:
                return 200, None

    @route('POST', '^/objects/(.+)/events$')
    def post_events_on_object(self, body, params):
        device_id = params[0]

        result = [self._process_event(event, False, device_id) for event in body]
        failed = filter(lambda r: r['result'] != "success", result)

        return 207 if failed else 200, result

    @route('GET', '^/events/exists/(.+)$')
    def get_events_exists(self, params):
        return 200, {params[0]: uuid.UUID(params[0]) in self.events}

    @route('POST', '^/events/exists$')
    def post_events_exist(self, body, _):
        return 200, [{id: uuid.UUID(id) in self.events} for id in body]

    # objects
    def _process_object(self, obj, overwrite=False):
        if 'x_device_id' not in obj:
            return {"result"}
        dev_id = obj['x_device_id']

        if 'x_object_type' not in obj:
            pass

        if dev_id in self.objects and not overwrite:
            pass

        obj['x_registration_date'] = datetime.now().isoformat()
        self.objects[dev_id] = obj

        return {"result": "success", "id": dev_id}

    @route('POST', '^/objects$')
    def post_one_object(self, body, _):
        result = self._process_object(body)
        if result['result'] != "success":
            return 400, result["message"]
        else:
            return 201, body

    @route('PUT', '^/objects$')
    def put_batch_objects(self, body, _):
        result = [self._process_object(obj, True) for obj in body]
        failed = filter(lambda r: r['result'] != "success", result)
        return 207 if failed else 200, result

    @route('PUT', '^/objects/(.+)$')
    def put_object_by_id(self, body, params):
        dev_id = params[0]
        self.objects[dev_id] = body
        return 200, None

    @route('DELETE', '^/objects/(.+)$')
    def delete_objects(self, body, params):
        dev_id = params[0]
        if body and 'x_timestamp' in body:
            pass

        if dev_id in self.objects:
            del self.objects[dev_id]

        return 200, None

    @route('GET', '^/objects/exists/(.+)$')
    def get_objects_exists(self, params):
        dev_id = params[0]
        return 200, {dev_id: dev_id in self.objects}

    @route('POST', '^/objects/exists$')
    def post_objects_exists(self, body, _):
        return 200, [{dev_id: dev_id in self.objects} for dev_id in body]

    # owners
    def _process_owner(self, owner):
        if 'username' not in owner:
            return {"result": "error", "message": ""}

        username = owner['username']
        if username in self.owners:
            return {"result": "error", "message": ""}

        owner['x_registration_date'] = datetime.now().isoformat()
        self.owners[username] = owner

        return {"result": "success", "id": username}

    @route('POST', '^/owners/?$')
    def post_one_owner(self, body, _):
        result = self._process_owner(body)
        if result['result'] != 'success':
            return 400, result['message']
        else:
            return 201, self.owners[body['username']]

    @route('PUT', '^/owners$')
    def put_owners(self, body, _):
        result = [self._process_owner(owner) for owner in body]
        failed = filter(lambda r: 'result' in r and r['result'] == "error", result)
        return 207 if failed else 200, result

    @route('PUT', '^/owners/(.+)$')
    def put_owner_by_id(self, body, params):
        username = params[0]
        if username in self.owners:
            self.owners[username] = body
        return 200, None

    @route('DELETE', '^/owners/(.+)$')
    def delete_owners(self, body, params):
        username = params[0]
        if body and 'x_timestamp' in body:
            pass

        if username in self.objects:
            del self.objects[username]

        return 200, None

    @route('POST', '^/owners/(.+)/objects/(.+)/claim$')
    def post_owners_claim(self, _, params):
        username, device_id = params

        if username not in self.owners:
            return 400, ""

        if device_id not in self.objects:
            return 400, ""

        self.objects[device_id]['x_owner'] = username
        return 200, None

    @route('POST', '^/owners/(.+)/password$')
    def put_owners_password(self, body, params):
        username = params[0]

        if username not in self.owners:
            return 400, ""

        if 'x_password' not in body:
            return 400, ""

        self.owners[username]['x_password'] = body['x_password']
        return 200, None

    @route('GET', '^/owners/exists/(.+)')
    def get_owner_exists(self, params):
        username = params[0]
        return 200, {username: username in self.owners}

    @route('POST', '^/owners/exists/?$')
    def post_owners_exist(self, body, _):
        return 200, [{username: username in self.owners} for username in body]

    # search
    def post_search_basic(self, body, params):
        raise NotImplementedError

    def post_search_validate(self, body, params):
        raise NotImplementedError

    def get_datasets(self, params):
        raise NotImplementedError
