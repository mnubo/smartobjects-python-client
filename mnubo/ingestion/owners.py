from mnubo.results import Result


class OwnersService(object):

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

    def create_update(self, owners):
        r = self.api_manager.post('owners', owners)
        r.raise_for_status()
        return [Result(*result) for result in r.json()]

    def delete(self, username):
        """ Deletes an owner from mnubo

        :param username: the username of the owner to be deleted
        """

        return self.api_manager.delete('owners/' + username)

    def owner_exists(self, owner_id):
        """
        :param owner_id (str|list): the owner_id or the list of owner_ids we want to check if existing
        :return:
        """

        r = self.api_manager.get('objects/exists/{0}'.format(owner_id))
        r.raise_for_status()

        return r.json()

    def owners_exist(self, owner_ids):
        """
        :param owner_id (str|list): the owner_id or the list of owner_ids we want to check if existing
        :return:
        """

        r = self.api_manager.post('objects/exists', owner_ids)
        r.raise_for_status()

        return r.json()
