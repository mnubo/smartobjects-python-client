from smartobjects.bigdata import StartExport, StreamPage

class BigDataService(object):
    def __init__(self, api_manager):
        """ Initializes BigData with the api manager
        """

        self.api_manager = api_manager

    def start_export(self, query):
        return StartExport(self.api_manager.post("bigdata/startexport", query).json())


    def stream_page(self, page_id):
        return StreamPage(self.api_manager.get("bigdata/streampage/{}".format(page_id)).json())