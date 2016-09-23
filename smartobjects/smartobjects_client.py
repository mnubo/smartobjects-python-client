
from smartobjects.ingestion.events import EventsService
from smartobjects.ingestion.owners import OwnersService
from smartobjects.ingestion.objects import ObjectsService
from smartobjects.restitution.search import SearchService
from smartobjects.api_manager import APIManager


class Environments:
    Sandbox = "https://rest.sandbox.mnubo.com"
    Production = "https://rest.api.mnubo.com"


class SmartObjectsClient(object):
    """ Initializes the smartobjects client which contains the API manager as well as the available resource services
    """

    def __init__(self, client_id, client_secret, environment, compression_enabled=True):
        """ Initialization of the smartobjects client

        The client exposes the Events, Objects, Owners and Search services.
        Initialization will fetch an API token with the id and secret provided.

        :param client_id (string): client_id part of the OAuth 2.0 credentials (available in your dashboard)
        :param client_secret (string): client_secret part of the OAuth 2.0 credentials (available in your dashboard)
        :param environment: either Environments.Sandbox or Environments.Production
            (note: client_id and client_secret are unique per environment)
        :param compression_enabled: gzip compress the request body (default: True)

        :note: Do not expose publicly code containing your client_id and client_secret
        .. seealso:: examples/simple_workflow.py
        """

        if environment not in (Environments.Sandbox, Environments.Production):
            raise ValueError("Invalid 'environment' argument, must be one of: Environments.Sandbox, Environments.Production")

        self._api_manager = APIManager(client_id, client_secret, environment, compression_enabled)
        self.owners = OwnersService(self._api_manager)
        self.events = EventsService(self._api_manager)
        self.objects = ObjectsService(self._api_manager)
        self.search = SearchService(self._api_manager)
