import uuid


class Result(object):
    """ Result object containing the information returned by an API call to Object or Owner services

    .. seealso:: EventResult

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
    def id(self) -> str:
        """identifier of the operation (deviceId for an object, username for an owner)"""
        return self._id

    @property
    def message(self) -> str:
        """If `result` is not `success`: contains the reason of the failure"""
        return self._message

    @property
    def result(self) -> str:
        """status of the operation: `success` or `failure`"""
        return self._result


class EventResult(Result):
    def __init__(self, *args, **kwargs):
        """Specialized version of `Result` for the EventsService

        `result` property can be `success`, `failure`, `conflict`, `notfound`
        """
        super(EventResult, self).__init__(*args, **kwargs)
        if self._id:
            self._id = uuid.UUID(self._id)
        self._object_exists = self._source.get('objectExists', None)

    @property
    def object_exists(self) -> bool:
        """`True` if the object specified by x_object.x_device_id actually exists.

        To prevent submitting events to non_existing object, use `must_exist=True` with `send()`
        """
        return self._object_exists
