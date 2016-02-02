

class OwnerServices(object):

    def __init__(self, api_manager):
        """ Initializes OwnerServices with the api manager
        """

        self.api_manager = api_manager

    def create(self, owner):
        """ Creates a new owner for mnubo

        :param owner: the owner of the object to be deleted
        """

        return self.api_manager.post('owners', owner)

    def claim(self, username, device_id):
        """ Owner claims an object

        :param username: the username of the owner claiming the object
        :param device_id: the device_id of the object being claimed
        """

        return self.api_manager.post('owners/' + username + '/objects/' + device_id + '/claim')

    def update(self, owner):
        """ Updates an owner from mnubo

        :param owner: the owner with the updated properties
        """

        return self.api_manager.put('owners/' + owner['username'], owner)

    def delete(self, username):
        """ Deletes an owner from mnubo

        :param username: the username of the owner to be deleted
        """

        return self.api_manager.delete('owners/' + username)


class ObjectServices(object):

    def __init__(self, api_manager):
        """ Initializes ObjectServices with the api manager
        """

        self.api_manager = api_manager

    def create(self, object):
        """ Creates a new object for mnubo

        :param object: the object to be created
        """

        return self.api_manager.post('objects', object)

    def update(self, object):
        """ Updates an object from mnubo

        :param object: the object with the updated properties
        """

        return self.api_manager.put('objects/'+object['x_device_id'], object)

    def delete(self, device_id):
        """ Deletes an object from mnubo

        :param device_id: the device_id of the object to be deleted
        """

        return self.api_manager.delete('objects/'+device_id)


class EventServices(object):

    def __init__(self, api_manager):
        """ Initializes EventServices with the api manager
        """

        self.api_manager = api_manager

    def send(self, event):
        """ Sends an event to mnubo

        :param event: an event object containing the properties requested by mnubo
        """

        return self.api_manager.post('events', event)


class SearchServices(object):

    def __init__(self, api_manager):
        """ Initializes SearchServices with the api manager
        """

        self.api_manager = api_manager

    def search(self, query):
        """ Sends a basic search query

        :param query: the query in json
        """

        return self.api_manager.post('search/basic', query)

    def search_datasets(self, query):
        """ Sends a search query on the dataset list

        :param query: the query in json
        """

        return self.api_manager.get('search/datasets', query)

