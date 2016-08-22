import uuid
from mnubo.results import EventResult


class EventsService(object):
    def __init__(self, api_manager):
        """ Initializes EventServices with the api manager
        """

        self.api_manager = api_manager

    def send(self, event, must_exist=False, report_results=False):
        """ Sends list of events to mnubo

        :param event: a list of dictionaries representing the events to be sent
        :return: list of EventResult
        """

        params = []
        if must_exist:
            params.append("must_exist=true")
        if report_results:
            params.append("report_results=true")

        path = "events?{0}".format('&'.join(params)) if params else "events"

        r = self.api_manager.post(path, event)
        r.raise_for_status()

        return [EventResult(**result) for result in r.json()]

    def event_exists(self, event_id):
        """
        :param event_id (uuid): the event_id we want to check if existing
        :return: bool
        """
        assert isinstance(event_id, uuid.UUID)
        str_id = str(event_id)

        r = self.api_manager.get('events/exists/{0}'.format(str_id))
        r.raise_for_status()
        json = r.json()

        assert str_id in json and isinstance(json[str_id], bool)
        return json[str_id]

    def events_exist(self, event_ids):
        """
        :param event_ids (list): the the list of event_ids we want to check if existing
        :return: dictionary with the event_id as the key and a boolean as the value
        """

        assert all(isinstance(id, uuid.UUID) for id in event_ids)

        r = self.api_manager.post('events/exists', event_ids)
        r.raise_for_status()

        return {uuid.UUID(key): value for key, value in r.json().iteritems()}
