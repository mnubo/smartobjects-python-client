from mnubo.ingestion.events import EventsService
from mnubo.ingestion.objects import ObjectsService
from mnubo.ingestion.owners import OwnersService
from mnubo.restitution.search import SearchService
from mnubo.api_manager import APIManager

__version__ = "2.0.0"


class Environments:
    Sandbox = "https://rest.sandbox.mnubo.com"
    Production = "https://rest.api.mnubo.com"


class MnuboClient(object):
    """ Initializes the mnubo client which contains the API manager as well as the available resource services
    """

    def __init__(self, client_id, client_secret, environment):

        if environment not in (Environments.Sandbox, Environments.Production):
            raise ValueError("Invalid 'environment' argument, must be one of: Environments.Sandbox, Environments.Production")

        self.__api_manager = APIManager(client_id, client_secret, environment)
        self.owners = OwnersService(self.__api_manager)
        self.events = EventsService(self.__api_manager)
        self.smart_objects = ObjectsService(self.__api_manager)
        self.search = SearchService(self.__api_manager)
