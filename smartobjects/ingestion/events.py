import uuid
from typing import List, Any, Dict, Optional

from smartobjects.api_manager import APIManager
from smartobjects.ingestion import EventResult


class EventsService(object):
    def __init__(self, api_manager: APIManager):
        """ Initializes EventServices with the api manager
        """

        self.api_manager = api_manager
        self.api_version = "/api/v3"

    def send(self, events: List[Dict[str, Any]], must_exist: bool = False, report_results: bool = True) -> Optional[
        List[EventResult]]:
        """ Sends list of events to smartobjects

        https://smartobjects.mnubo.com/documentation/api_ingestion.html#post-api-v3-events-batch

        :param events: a list of dictionaries representing the events to be sent
        :param must_exist (bool): toggles checking that the device actually exist
            if True, event will be rejected if no object can be matched, otherwise it will be processed
        :param report_results (bool): toggles if we should return a list of EventResult with the status of event
            sent (success, failure, conflict, notfound)
            if False, an exception will be raised if at least one event failed, None otherwise
            see https://smartobjects.mnubo.com/documentation/api_ingestion.html#post-api-v3-events for more details
        :return: list of EventResult or None (report_results=False)
        """
        self._validate_event_list(events)
        [self._validate_event(event) for event in events]

        params = []
        if must_exist:
            params.append("must_exist=true")
        if report_results:
            params.append("report_results=true")

        path = f"{self.api_version}/events?{'&'.join(params)}" if params else "events"

        r = self.api_manager.post(path, self._ensure_serializable(events))

        return [EventResult(**result) for result in r.json()] if report_results else None

    def send_from_device(self, device_id: str, events: List[Dict[str, Any]], report_results: bool = True) -> Optional[
        List[EventResult]]:
        """ Sends a list of events directly associated with an object

        https://smartobjects.mnubo.com/documentation/api_ingestion.html#post-api-v3-objects-x-device-id-events
        With this version, it is no longer required to include x_object.x_device_id in each event.

        :param device_id: deviceId of the targeted object
        :param events: a list of dictionaries representing the events to be sent
        :param report_results (bool): toggles if we should return a list of EventResult with the status of event
            sent (success, failure, conflict, notfound)
            if False, an exception will be raised if at least one event failed, None otherwise
            see https://smartobjects.mnubo.com/documentation/api_ingestion.html#post-api-v3-events for more details
        :return: list of EventResult or None (report_results=False)
        """
        self._validate_event_list(events)
        if not device_id:
            raise ValueError("device_id cannot be null or empty.")
        if not all(['x_event_type' in event and event['x_event_type'] for event in events]):
            raise ValueError("x_event_type cannot be null or empty.")

        path = f"{self.api_version}/objects/{device_id}/events"
        if report_results:
            path += "?report_results=true"
        r = self.api_manager.post(path, self._ensure_serializable(events))

        return [EventResult(**result) for result in r.json()] if report_results else None

    def event_exists(self, event_id: str) -> bool:
        """ Checks if an event with UUID `uuid_id` exists in the platform

        :param event_id (uuid): the event_id we want to check if existing
        :return: True if the event actually exist in the platform, False otherwise
        """
        assert isinstance(event_id, uuid.UUID)
        str_id = str(event_id)
        r = self.api_manager.get(f'{self.api_version}/events/exists/{str_id}')
        json = r.json()

        assert str_id in json and isinstance(json[str_id], bool)
        return json[str_id]

    def events_exist(self, event_ids: List[uuid.UUID]) -> Dict[uuid.UUID, bool]:
        """ Checks if events with UUID as specified in `event_ids` exist in the platform

        :param event_ids (list): list of event_ids we want to check if existing
        :return: dictionary with the event_id as the key and a boolean as the value
        """

        assert all(isinstance(id, uuid.UUID) for id in event_ids)

        r = self.api_manager.post(f'{self.api_version}/events/exists', [str(id) for id in event_ids])
        return {uuid.UUID(key): value for entry in r.json() for key, value in entry.items()}

    def _validate_event(self, event: Dict[str, Any]):
        if 'x_object' not in event or 'x_device_id' not in event['x_object'] or not event['x_object']['x_device_id']:
            raise ValueError("x_object.x_device_id cannot be null or empty.")

        if 'x_event_type' not in event or not event['x_event_type']:
            raise ValueError("x_event_type cannot be null or empty.")

    def _validate_event_list(self, events: List[Dict[str, Any]]):
        if not events:
            raise ValueError("Event list cannot be null or empty.")

        if not isinstance(events, list) or not all([isinstance(e, dict) for e in events]):
            raise ValueError("Invalid argument type for event list")

        unique = set()
        for event in filter(lambda e: 'event_id' in e, events):
            if event['event_id'] in unique:
                raise ValueError(f"The event_id [{event['event_id']}] is duplicated in the list")
            else:
                unique.add(event['event_id'])

    def _ensure_serializable(self, events: List[Dict[str, str]]) -> List[Dict[str, str]]:
        def on_event(e) -> Dict[str, str]:
            if 'event_id' in e:
                e['event_id'] = str(e['event_id'])
            return e

        return [on_event(e) for e in events]
