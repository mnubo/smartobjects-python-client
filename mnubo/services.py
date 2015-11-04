import json

# MNUOwner

class MNUOwnerServices(object):

    def __init__(self, api_manager):
        self.api_manager = api_manager

    def create(self, owner):
        return self.api_manager.post('owners', owner.__dict__)

    def claim(self, username, device_id):
        return self.api_manager.post('owners/' + username + '/objects/' + device_id + '/claim')

    def update(self, owner):
        return self.api_manager.put('owners/' + owner.username, owner.__dict__)

    def delete(self, username):
        return self.api_manager.delete('owners/' + username)


# MNUSmartObject
class MNUSmartObjectServices(object):

    def __init__(self, api_manager):
        self.api_manager = api_manager

    def create(self, smart_object):
        return self.api_manager.post('objects', smart_object.__dict__)

    def update(self, smart_object):
        return self.api_manager.put('objects/'+smart_object.x_device_id, smart_object.__dict__)

    def delete(self, device_id):
        return self.api_manager.delete('objects/'+device_id)


# MNUEvent
class MNUEventServices(object):

    def __init__(self, api_manager):
        self.api_manager = api_manager

    def send(self, event):
        return self.api_manager.post('events', event.__dict__)

