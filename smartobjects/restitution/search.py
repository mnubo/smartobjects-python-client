from smartobjects.restitution import QueryValidationResult, ResultSet, DataSet


class SearchService(object):
    def __init__(self, api_manager):
        """ Initializes SearchServices with the api manager
        """

        self.api_manager = api_manager

        self.api_version = '/api/v3'

    def search(self, query):
        """ Sends a basic search query

        see https://smartobjects.mnubo.com/documentation/api_search.html#post-api-v3-search-basic for more details

        :param query (dict): the search query
        :returns: ResultSet object
        .. seealso:: ResultSet

        Example:
        >>> resultset = client.search.search({"from": "event", "select": [{"value": "speed"}]})
        >>> f"Got {len(resultset)} results!")
        Got 42 results!
        """
        r = self.api_manager.post(f'{self.api_version}/search/basic', query)
        return ResultSet(r.json())

    def get_datasets(self):
        """ Retrieves the datasets available for the current namespace

        https://smartobjects.mnubo.com/documentation/api_search.html#get-api-v3-search-datasets

        :returns: dictionary of Dataset objects: {'dataset name': Dataset}

        Example:
        >>> datasets = client.search.get_datasets()
        >>> datasets['events'].fields[0].key
        temperature
        """
        r = self.api_manager.get(f'{self.api_version}/search/datasets')
        return {dataset['key']: DataSet(dataset) for dataset in r.json()}

    def validate_query(self, query):
        """ Validates the search query for easier development and reduced errors

        :param query (dict): the search query to be validated

        Example:
        >>> result = client.search.validate_query({"fro": "event", "select": [{"value": "speed"}]})
        >>> result.is_valid, result.validation_errors
        (False, ["a query must have a 'from' field"])
        """
        r = self.api_manager.post(f'{self.api_version}/search/validateQuery', query)
        return QueryValidationResult(r.json())
