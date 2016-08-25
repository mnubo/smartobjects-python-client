from mnubo.results import Result


class OwnersService(object):

    def __init__(self, api_manager):
        """ Initializes OwnerServices with the api manager
        """

        self.api_manager = api_manager

    def validate_owner(self, owner):
        if not owner:
            raise ValueError("Owner body cannot be null")
        if 'username' not in owner or not owner['username']:
            raise ValueError("username cannot be blank.")

    def create(self, owner):
        """ Creates a new owner for mnubo

        :param owner: the owner of the object to be deleted
        """
        self.validate_owner(owner)
        self.api_manager.post('owners', owner)

    def claim(self, username, device_id):
        """ Owner claims an object

        :param username: the username of the owner claiming the object
        :param device_id: the device_id of the object being claimed
        """
        if not username:
            raise ValueError("username cannot be blank.")
        if not device_id:
            raise ValueError("deviceId cannot be blank.")
        self.api_manager.post('owners/{}/objects/{}/claim'.format(username, device_id))

    def update(self, username, owner):
        """ Updates an owner from mnubo

        :param owner: the owner with the updated properties
        """
        if not username:
            raise ValueError("username cannot be blank.")
        if not owner:
            raise ValueError("Object body cannot be blank.")

        self.api_manager.put('owners/{}'.format(username), owner)

    def create_update(self, owners):
        """

        :param owners:
        :return:
        """
        [self.validate_owner(owner) for owner in owners]

        r = self.api_manager.put('owners', owners)
        return [Result(**result) for result in r.json()]

    def delete(self, username):
        """ Deletes an owner from mnubo

        :param username: the username of the owner to be deleted
        """
        if not username:
            raise ValueError("username cannot be blank.")

        return self.api_manager.delete('owners/{}'.format(username))

    def owner_exists(self, username):
        """
        :param username (str|list): username we want to check if existing
        :return:
        """
        if not username:
            raise ValueError("username cannot be blank.")

        r = self.api_manager.get('owners/exists/{}'.format(username))
        json = r.json()
        assert username in json
        return json[username]

    def owners_exist(self, usernames):
        """
        :param usernames: list of usernames we want to check if existing
        :return:
        """
        if not usernames:
            raise ValueError("List of username cannot be blank.")
        r = self.api_manager.post('owners/exists', usernames)
        return reduce(lambda x, y: dict(x.items() + y.items()), r.json())
