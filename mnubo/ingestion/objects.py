
class ObjectsService(object):

    def __init__(self, api_manager):
        """ Initializes ObjectServices with the api manager
        """

        self.api_manager = api_manager

    def require_not_blank(self, property, object, message):
        pass

    def create(self, object):
        """ Creates a new object for mnubo

        :param object: the object to be created
        """
        if 'x_device_id' not in object or not object['x_device_id']:
            raise ValueError('x_device_id cannot be blank.')

        self.api_manager.post('objects', object).raise_for_status()

    def update(self, object):
        """ Updates an object from mnubo

        :param object: the object with the updated properties
        """

        return self.api_manager.put('objects/'+object['x_device_id'], object)

    def create_update(self, objects):
        """ create or update a batch of objects

        a single batch can contain up to 1000 objects.

        :param objects (list): list or objects to be sent to mnubo. If the object already exists, it will be
            updated with the new content, otherwise it will be created
        :return:
        """

        r = self.api_manager.put('objects/', objects)
        r.raise_for_status()
        return r.json()

    def delete(self, device_id):
        """ Deletes an object from mnubo

        :param device_id: the device_id of the object to be deleted
        """

        return self.api_manager.delete('objects/'+device_id)

    def exists(self, device_id):
        """

        :param device_id (str|list): the device_id or the list of device_ids we want to check if existing
        :return:
        """

        if isinstance(device_id, basestring):
            r = self.api_manager.get('objects/exists/{0}'.format(device_id))
        elif all(isinstance(dev_id, basestring) for dev_id in device_id):
            r = self.api_manager.post('objects/exists', device_id)
        else:
            raise TypeError

        r.raise_for_status()
        return r.json()


    def object_exist(self, device_id):
        pass


    def objects_exist(self, device_ids):
        pass