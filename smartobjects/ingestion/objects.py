from smartobjects.ingestion import Result

class ObjectsService(object):

    def __init__(self, api_manager):
        """ Initializes ObjectServices with the api manager
        """

        self.api_manager = api_manager

    def _validate_object(self, object, validate_object_type=True):
        if not object:
            raise ValueError('Object body cannot be null.')

        if 'x_device_id' not in object or not object['x_device_id']:
            raise ValueError('x_device_id cannot be null or empty.')

        if validate_object_type and ('x_object_type' not in object or not object['x_object_type']):
            raise ValueError('x_object_type cannot be null or empty.')

    def create(self, object):
        """ Creates a new object in the smartobjects platform

        :param object: dictionary representing the object to be created
        """
        self._validate_object(object)
        self.api_manager.post('objects', object)

    def update(self, device_id, object):
        """ Updates an object in the smartobjects platform

        :param device_id: deviceId of the targeted object
        :param object: the dict with the updated properties (will be merged with existing properties)
            if x_object.x_device_id is present in the object, it will be ignored
        """
        if not device_id:
            raise ValueError("deviceId cannot be null or empty.")
        if not object:
            raise ValueError("Object body cannot be null or empty.")
        self.api_manager.put('objects/{}'.format(device_id), object)

    def create_update(self, objects):
        """ create or update a batch of objects

        https://smartobjects.mnubo.com/apps/doc/api_ingestion.html#put-api-v3-objects-batch
        a single batch can contain up to 1000 objects.

        :param objects: list of objects to be sent to smartobjects. If the object already exists, it will be
            updated with the new content, otherwise it will be created
        :return: list of Result objects with the status of each operations
        """
        [self._validate_object(obj, validate_object_type=False) for obj in objects]
        r = self.api_manager.put('objects', objects)
        return [Result(**result) for result in r.json()]

    def delete(self, device_id):
        """ Deletes an object from the platform

        :param device_id: the device_id of the object to be deleted
        """
        if not device_id:
            raise ValueError('x_device_id cannot be null or empty.')
        self.api_manager.delete('objects/{}'.format(device_id))

    def object_exists(self, device_id):
        """ Checks if an object with deviceId `uuid_id` exists in the platform

        :param device_id (string): the deviceId we want to check if existing
        :return: True if the object actually exist in the platform, False otherwise
        """

        if not device_id:
            raise ValueError('deviceId cannot be null or empty.')
        r = self.api_manager.get('objects/exists/{0}'.format(device_id))
        json = r.json()
        assert device_id in json
        return json[device_id]

    def objects_exist(self, device_ids):
        """ Checks if events with deviceIds as specified in `device_ids` exist in the platform

        :param device_ids (list): list of deviceIds we want to check if existing
        :return: result dict with the deviceId as the key and a boolean as the value
        """

        if not device_ids:
            raise ValueError('List of deviceId cannot be null or empty.')
        r = self.api_manager.post('objects/exists', device_ids)

        result = {}
        for object in r.json():
            result.update(object)
        return result
