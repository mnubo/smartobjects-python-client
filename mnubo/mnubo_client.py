
from ingestion.events import EventsService
from ingestion.owners import OwnersService
from ingestion.objects import ObjectsService
from restitution.search import SearchService
from api_manager import APIManager


class Environments:
    Sandbox = "https://rest.sandbox.mnubo.com"
    Production = "https://rest.api.mnubo.com"


class MnuboClient(object):
    """ Initializes the mnubo client which contains the API manager as well as the available resource services
    """

    def __init__(self, client_id, client_secret, environment):

        if environment not in (Environments.Sandbox, Environments.Production):
            raise ValueError("Invalid 'environment' argument, must be one of: Environments.Sandbox, Environments.Production")

        self._api_manager = APIManager(client_id, client_secret, environment)
        self.owners = OwnersService(self._api_manager)
        self.events = EventsService(self._api_manager)
        self.objects = ObjectsService(self._api_manager)
        self.search = SearchService(self._api_manager)
