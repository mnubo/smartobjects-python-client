
class SearchService(object):

    def __init__(self, api_manager):
        """ Initializes SearchServices with the api manager
        """

        self.api_manager = api_manager

    def search(self, query):
        """ Sends a basic search query

        :param query: the query in json
        """

        return self.api_manager.post('search/basic', query)

    def get_datasets(self):
        """ Sends a search query on the dataset list

        :param query: the query in json
        """

        return self.api_manager.get('search/datasets')

    def validate_query(self, query):
        pass
