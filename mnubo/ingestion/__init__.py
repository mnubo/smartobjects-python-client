import uuid


class Result(object):
    """ Result object containing the information returned by an API call to Object/Owner/Search services

    :seealso: EventResult

    Result object can be constructed either by passing a dictionary as the only argument (usually returned by an API HTTP call)
     >>> success = Result({'id': 'device_id', 'result': 'success'})
     >>> failure = Result({'id': 'device_id', 'result': 'error', 'message': 'Invalid property "some invalid property"'})
    Or via named arguments:
     >>> success = Result(id='device_id', result='success')
     >>> failure = Result(id='device_id', result='error', message='Invalid property "some invalid property"')
    """
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], dict):
            self._source = args[0]
        elif not args and kwargs:
            self._source = kwargs
        else:
            raise ValueError()

        self._id = self._source.get('id', None)
        self._result = self._source.get('result', None)
        self._message = self._source.get('message', None)

    @property
    def id(self):
        return self._id

    @property
    def message(self):
        return self._message

    @property
    def result(self):
        return self._result


class EventResult(Result):
    def __init__(self, *args, **kwargs):
        super(EventResult, self).__init__(*args, **kwargs)
        if self._id:
            self._id = uuid.UUID(self._id)
        self._object_exists = self._source.get('objectExists', None)

    @property
    def object_exists(self):
        return self._object_exists

