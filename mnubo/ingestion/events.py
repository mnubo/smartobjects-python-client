import uuid
from mnubo.ingestion import EventResult


class EventsService(object):
    def __init__(self, api_manager):
        """ Initializes EventServices with the api manager
        """

        self.api_manager = api_manager

    def validate_event(self, event):
        if 'x_object' not in event or 'x_device_id' not in event['x_object'] or not  event['x_object']['x_device_id']:
            raise ValueError("x_object.x_device_id cannot be null or empty.")

        if 'x_event_type' not in event or not event['x_event_type']:
            raise ValueError("x_event_type cannot be null or empty.")

    def validate_event_list(self, events):
        if not events:
            raise ValueError("Event list cannot be null or empty.")

        if not isinstance(events, list) or not all([isinstance(e, dict) for e in events]):
            raise ValueError("Invalid argument type for event list")

        unique = set()
        for event in filter(lambda e: 'event_id' in e, events):
            if event['event_id'] in unique:
                raise ValueError("The event_id [{}] is duplicated in the list".format(event['event_id']))
            else:
                unique.add(event['event_id'])

    def ensure_serializable(self, events):
        def on_event(e):
            if 'event_id' in e:
                e['event_id'] = str(e['event_id'])
            return e
        return [on_event(e) for e in events]

    def send(self, events, must_exist=False, report_results=True):
        """ Sends list of events to mnubo

        :param events: a list of dictionaries representing the events to be sent
        :return: list of EventResult
        """
        self.validate_event_list(events)
        [self.validate_event(event) for event in events]

        params = []
        if must_exist:
            params.append("must_exist=true")
        if report_results:
            params.append("report_results=true")

        path = "events?{0}".format('&'.join(params)) if params else "events"

        r = self.api_manager.post(path, self.ensure_serializable(events))

        return [EventResult(**result) for result in r.json()] if report_results else None

    def send_from_device(self, device_id, events, report_results=True):
        """
        https://sop.mtl.mnubo.com/apps/doc/api.html#post-api-v3-objects-x-device-id-events

        :param device_id:
        :param events:
        :return:
        """
        self.validate_event_list(events)
        if not device_id:
            raise ValueError("device_id cannot be null or empty.")
        if not all(['x_event_type' in event and event['x_event_type'] for event in events]):
            raise ValueError("x_event_type cannot be null or empty.")

        path = "objects/{}/events".format(device_id)
        if report_results:
            path += "?report_results=true"
        r = self.api_manager.post(path, self.ensure_serializable(events))

        return [EventResult(**result) for result in r.json()] if report_results else None

    def event_exists(self, event_id):
        """
        :param event_id (uuid): the event_id we want to check if existing
        :return: bool
        """
        assert isinstance(event_id, uuid.UUID)
        str_id = str(event_id)

        r = self.api_manager.get('events/exists/{0}'.format(str_id))
        json = r.json()

        assert str_id in json and isinstance(json[str_id], bool)
        return json[str_id]

    def events_exist(self, event_ids):
        """
        :param event_ids (list): the the list of event_ids we want to check if existing
        :return: dictionary with the event_id as the key and a boolean as the value
        """

        assert all(isinstance(id, uuid.UUID) for id in event_ids)

        r = self.api_manager.post('events/exists', [str(id) for id in event_ids])
        return {uuid.UUID(key): value for key, value in r.json().iteritems()}
