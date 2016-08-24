import uuid



class BatchServices(object):

    def __init__(self, api_manager):
        """ Initializes BatchServices with the api manager
        """

        self.api_manager = api_manager

    def owners(self, owners):
        """ Creates or updates owners in batch

        :param owners: the owners to be created
        """

        return self.api_manager.put('owners', owners, False)

    def objects(self, objects):
        """ Creates or updates objects in batch

        :param objects: the objects to be created
        """

        return self.api_manager.put('objects', objects, False)

    def events(self, events, report_results=False):
        """ Creates events in batch

        :param events: the events to be created
        :param report_results: returns a body with the result of each individual event
        """
        show_report = 'true' if report_results else 'false'

        return self.api_manager.post('events?report_results='+show_report, events)
