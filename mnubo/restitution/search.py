from mnubo.restitution import QueryValidationResult, ResultSet, DataSet


class SearchService(object):
    def __init__(self, api_manager):
        """ Initializes SearchServices with the api manager
        """

        self.api_manager = api_manager

    def search(self, query):
        """ Sends a basic search query

        :param query: the query in json
        """
        r = self.api_manager.post('search/basic', query)
        return ResultSet(r.json())

    def get_datasets(self):
        """ Sends a search query on the dataset list

        :param query: the query in json
        """
        r = self.api_manager.get('search/datasets')
        return {dataset['key']: DataSet(dataset) for dataset in r.json()}

    def validate_query(self, query):
        r = self.api_manager.post('search/validateQuery', query)
        return QueryValidationResult(r.json())

