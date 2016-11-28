from smartobjects.ingestion import Result


class OwnersService(object):

    def __init__(self, api_manager):
        """ Initializes OwnerServices with the api manager
        """

        self.api_manager = api_manager

    def _validate_owner(self, owner):
        if not owner:
            raise ValueError("Owner body cannot be null")
        if 'username' not in owner or not owner['username']:
            raise ValueError("username cannot be null or empty.")

    def create(self, owner):
        """ Creates a new owner in the smartobjects platform

        :param owner: the owner of the object to be deleted
        """
        self._validate_owner(owner)
        self.api_manager.post('owners', owner)

    def claim(self, username, device_id):
        """ Owner claims an object

        https://sop.mtl.mnubo.com/apps/doc/api.html#post-api-v3-owners-username-objects-x-device-id-claim

        :param username: the username of the owner claiming the object
        :param device_id: the device_id of the object being claimed
        """
        if not username:
            raise ValueError("username cannot be null or empty.")
        if not device_id:
            raise ValueError("device_id cannot be null or empty.")
        self.api_manager.post('owners/{}/objects/{}/claim'.format(username, device_id))

    def unclaim(self, username, device_id):
        """ Owner unclaims an object

        https://sop.mtl.mnubo.com/apps/doc/api.html#post-api-v3-owners-username-objects-x-device-id-unclaim

        :param username: the username of the owner whom owns the object
        :param device_id: the device_id of the object being unclaimed
        """
        if not username:
            raise ValueError("username cannot be null or empty.")
        if not device_id:
            raise ValueError("device_id cannot be null or empty.")
        self.api_manager.post('owners/{}/objects/{}/unclaim'.format(username, device_id))

    def update(self, username, owner):
        """ Updates an owner from smartobjects

        :param owner: the owner with the updated properties
        """
        if not username:
            raise ValueError("username cannot be null or empty.")
        if not owner:
            raise ValueError("Object body cannot be null or empty.")

        self.api_manager.put('owners/{}'.format(username), owner)

    def create_update(self, owners):
        """ Create or update a batch of owners at once

        https://sop.mtl.mnubo.com/apps/doc/api.html#put-api-v3-owners-batch

        :param owners: list of owners to be sent to the smartobjects platform. If the owner already exists, it will be
            updated with the new content, otherwise it will be created
        :return: list of Result objects with the status of each operation
        """
        [self._validate_owner(owner) for owner in owners]

        r = self.api_manager.put('owners', owners)
        return [Result(**result) for result in r.json()]

    def delete(self, username):
        """ Deletes an owner from the smartobjects platform

        :param username: the username of the owner to be deleted
        """
        if not username:
            raise ValueError("username cannot be null or empty.")

        return self.api_manager.delete('owners/{}'.format(username))

    def owner_exists(self, username):
        """ Checks if an owner with username `username` exists in the platform

        :param username (string): the username we want to check if existing
        :return: True if the owner actually exist in the platform, False otherwise
        """

        if not username:
            raise ValueError("username cannot be null or empty.")

        r = self.api_manager.get('owners/exists/{}'.format(username))
        json = r.json()
        assert username in json
        return json[username]

    def owners_exist(self, usernames):
        """ Checks if owners with usernames as specified in `usernames` exist in the platform

        :param usernames (list): list of owner username we want to check if existing
        :return: result dict with the username as the key and a boolean as the value
        """

        if not usernames:
            raise ValueError("List of username cannot be null or empty.")
        r = self.api_manager.post('owners/exists', usernames)

        result = {}
        for owner in r.json():
            result.update(owner)
        return result
