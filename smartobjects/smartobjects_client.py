from typing import Optional, Dict, Any

from smartobjects.api_manager import APIManager
from smartobjects.datalake.datasets import DatalakeService
from smartobjects.ingestion.events import EventsService
from smartobjects.ingestion.objects import ObjectsService
from smartobjects.ingestion.owners import OwnersService
from smartobjects.model.model import ModelService
from smartobjects.restitution.search import SearchService


class Environments:
    """ Provide default URL if you don't have a specific one
    """
    Sandbox = "https://aiot-sandbox.aspentech.ai"
    Production = "https://aiot-prod.aspentech.ai"


class ExponentialBackoffConfig(object):
    """Configuration for exponential backoff retries"""

    def __init__(self, number_of_attempts=5, initial_delay_in_seconds=0.5, on_retry=None):
        """ Config object for exponentional backoff retries

        :param number_of_attempts: maximum number of attempts (default: 5)
        :param initial_delay_in_seconds: initial delay in seconds to be incresed exponentially (default: 0.5 (500 millis))
        :param on_retry: function that takes two arguments called before a retry is attempted (func, trial_number) (default: None)
        """
        self.number_of_attempts = number_of_attempts
        self.initial_delay_in_seconds = initial_delay_in_seconds
        self.on_retry = on_retry


class SmartObjectsClient(object):
    """ Initializes the smartobjects client which contains the API manager as well as the available resource services
    """

    def __init__(self, client_id: Optional[str], client_secret: Optional[str], environment: str,
                 compression_enabled: bool = True,
                 backoff_config=None, token_override=None):
        """ Initialization of the smartobjects client

        The client exposes the Events, Objects, Owners and Search services.
        Initialization will fetch an API token with the id and secret provided.

        :param client_id (string): client_id part of the OAuth 2.0 credentials (available in your dashboard)
        :param client_secret (string): client_secret part of the OAuth 2.0 credentials (available in your dashboard)
        :param environment: a URL to the targeted environment (Environments.Sandbox or Environments.Production can be used)
            (note: client_id and client_secret are unique per environment)
        :param compression_enabled: gzip compress the request body (default: True)
        :param backoff_config: retry with exponential backoff (default: None)
        :param token_override: this token will be used instead of performing the OAuth2 dance with the client_id 
                               and client_secret. This is not recommended for production (default: None)

        :note: Do not expose publicly code containing your client_id and client_secret
        .. seealso:: examples/simple_workflow.py
        """

        if not environment:
            raise ValueError("environment cannot be null or empty.")

        self._api_manager = APIManager(client_id, client_secret, environment, compression_enabled, backoff_config,
                                       token_override)
        self.owners = OwnersService(self._api_manager)
        self.events = EventsService(self._api_manager)
        self.objects = ObjectsService(self._api_manager)
        self.search = SearchService(self._api_manager)
        self.model = ModelService(self._api_manager)
        self.datalake = DatalakeService(self._api_manager)

    @classmethod
    def withToken(cls, token: str, environment: str, compression_enabled: bool = True,
                  backoff_config: Optional[Dict[str, Any]] = None) -> "SmartObjectsClient":
        """ Initialization of the smartobjects client

        The client exposes the Events, Objects, Owners and Search services.
        Initialization will fetch an API token with the id and secret provided.

        :param client_id (string): client_id part of the OAuth 2.0 credentials (available in your dashboard)
        :param client_secret (string): client_secret part of the OAuth 2.0 credentials (available in your dashboard)
        :param environment: a URL to the targeted environment (Environments.Sandbox or Environments.Production can be used)
            (note: client_id and client_secret are unique per environment)
        :param compression_enabled: gzip compress the request body (default: True)
        :param backoff_config: retry with exponential backoff (default: None)

        :note: Do not expose publicly code containing your client_id and client_secret
        .. seealso:: examples/simple_workflow.py
        """
        return cls(client_id=None, client_secret=None, environment=environment, compression_enabled=compression_enabled,
                   backoff_config=backoff_config, token_override=token)
