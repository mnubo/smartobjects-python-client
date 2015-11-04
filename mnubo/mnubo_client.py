
from services import MNUEventServices
from services import MNUOwnerServices
from services import MNUSmartObjectServices
from api_manager import MNUAPIManager

class MnuboClient(object):

    def __init__(self, client_id, client_secret, hostname):
        self.__auth_manager = MNUAPIManager(client_id, client_secret, hostname)
        self.owner_services = MNUOwnerServices(self.__auth_manager)
        self.event_services = MNUEventServices(self.__auth_manager)
        self.smart_object_services = MNUSmartObjectServices(self.__auth_manager)

