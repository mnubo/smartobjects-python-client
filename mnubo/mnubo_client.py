
from services import EventServices
from services import OwnerServices
from services import ObjectServices
from services import SearchServices
from api_manager import APIManager


class MnuboClient(object):
    """ Initializes the mnubo client which contains the API manager as well as the available resource services
    """

    def __init__(self, client_id, client_secret, hostname):
        self.__api_manager = APIManager(client_id, client_secret, hostname)
        self.owner_services = OwnerServices(self.__api_manager)
        self.event_services = EventServices(self.__api_manager)
        self.smart_object_services = ObjectServices(self.__api_manager)
        self.search_services = SearchServices(self.__api_manager)

