class StreamPage(object):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], dict):
            self._source = args[0]
        elif not args and kwargs:
            self._source = kwargs
        else:
            raise ValueError("Unable to construct StartExport")

        self._next_page = self._source.get('nextPage', None)
        self._rows = self._source.get('rows', [])

    @property
    def next_page(self):
        """The next page you can stream, or None."""
        return self._next_page

    @property
    def rows(self):
        """
        An array of all the rows of the current page. A row has the column defined
        in the columns Array returned on the BigDataService.start_export(query)
        """
        return self._rows

class StartExport(object):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], dict):
            self._source = args[0]
        elif not args and kwargs:
            self._source = kwargs
        else:
            raise ValueError("Unable to construct StartExport")

        self._stream_first_pages = self._source.get('streamsFirstPages', [])
        self._columns = self._source.get('columns', [])

    @property
    def stream_first_pages(self):
        """
        An array of all the pages that can be streamed. A page can
        be used in a call to the `BigDataService.stream_page(page)`
        method.
        """
        return self._stream_first_pages

    @property
    def columns(self):
        """
        An array of all the columns you will find in a response from
        a stream page call.
        """
        return self._columns