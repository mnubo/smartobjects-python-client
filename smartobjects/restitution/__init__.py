from datetime import datetime


class ResultSet(object):
    def __init__(self, *args, **kwargs):
        """ Contains the result of a search query """

        if len(args) == 1 and isinstance(args[0], dict):
            self._source = args[0]
        elif not args and kwargs:
            self._source = kwargs
        else:
            raise ValueError("Invalid arguments")

        self._columns = self._source.get('columns', [])
        self._rows = self._source.get('rows', [])

        self._col_to_idx = {col['label']: idx for idx, col in enumerate(self._columns)}

    def __iter__(self):
        return iter([ResultRow(row, self) for row in self._rows])

    def __len__(self):
        return len(self._rows)

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise IndexError("item must be an integer")
        if not 0 <= item < len(self._rows):
            raise IndexError(f"Invalid index: must be in the range [{0}, {len(self._rows)})")
        return ResultRow(self._rows[item], self)

    def get_column_index(self, item: str) -> int:
        """Returns the column index associated with a given column name

        Example:
            >>> resultset.get_column_index("speed")
            0
        """
        if item not in self._col_to_idx:
            raise IndexError(f"Invalid column '{item}'")
        return self._col_to_idx[item]

    def get_column_type(self, item: str) -> int:
        """Returns the highLevelType associated with a given column name

        :rtype: str

        Example:
            >>> resultset.get_column_type("speed")
            double
        """
        idx = self.get_column_index(item)
        return self._columns[idx]['type']

    @property
    def raw(self):
        """raw JSON object as returned by the search API"""
        return self._source

    @property
    def columns(self):
        """list of dictionaries representing the columns with the `label` and `type` keys (order of columns is the same as in the rows)"""
        return self._columns

    @property
    def rows(self):
        """list of rows, itself containing a list of result values

        Example:
            >>> resultset.rows
            [[1, 2, 3], [4, 5, 6]]
        """
        return self._rows

    @property
    def df(self):
        """Returns the result set as a Pandas DataFrame if pandas is present. Otherwise return None.

        Example:
            >>> resultset.df
                             year  COUNT(*)
            0 2016-01-01 05:00:00      2155
            1 2017-01-01 05:00:00      1232
        """
        try:
            import pandas
            columns = [col['label'] for col in self._columns]
            dataframe = pandas.DataFrame(self._rows, columns=columns)
            for column in self._columns:
                id_col = column['label']
                if column['type'] == 'datetime':
                    dataframe[id_col] = pandas.to_datetime(dataframe[id_col], utc=True)

            return dataframe
        except ImportError:
            raise ImportError('The "pandas" package is required to use this feature')

    # type conversion utils
    @staticmethod
    def ToDatetime(date):
        return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")


class ResultRow(object):
    """ Single row of a ResultSet object """

    def __init__(self, row, parent_rs):
        self._source = row
        self._parent = parent_rs

    def __getitem__(self, item):
        return self.get(item)

    def get(self, item, rtype=None):
        """ Generic accessor to the row content

        Allows access with index or column name:
        >>> row.get(0)
        >>> row.get("speed")

        Raises an IndexError if out of bound or no such column

        Allows conversion of the value with the optional `rtype` argument:
        >>> row.get("speed", float)
        >>> row.get("speed", lambda x: x * miles_to_kmh_ratio)  # also with a lambda
        >>> row.get("timestamp", ResultSet.ToDatetime)          # shorthand to convert back to datetime
        """
        if isinstance(item, str):
            index = self._parent.get_column_index(item)
        elif isinstance(item, int):
            index = item
        else:
            raise ValueError("Invalid type for argument 'item'")

        if not 0 <= index < len(self._source):
            raise IndexError(f"Invalid index: must be in the range [{0}, {len(self._source)})")

        if rtype:
            return rtype(self._source[index])
        else:
            return self._source[index]

    @property
    def raw(self):
        return self._source


class DataSet(object):
    """
    https://smartobjects.mnubo.com/documentation/api_search.html#get-api-v3-search-datasets
    """

    def __init__(self, json):
        self._source = json
        self.key = self._source.get('key')
        self.description = self._source.get('key')
        self.display_name = self._source.get('displayName')
        self.fields = [Field(field) for field in self._source.get('fields', [])]


class Field(object):
    """
    https://smartobjects.mnubo.com/documentation/api_search.html#get-api-v3-search-datasets
    """

    def __init__(self, json):
        self._source = json
        self.key = self._source.get('key')
        self.high_level_type = self._source.get('highLevelType')
        self.display_name = self._source.get('displayName')
        self.description = self._source.get('description')
        self.container_type = self._source.get('containerType')
        self.primary_key = self._source.get('primaryKey')


class QueryValidationResult(object):
    """ Contains the result of a call to validate_query """

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], dict):
            self._source = args[0]
        elif not args and kwargs:
            self._source = kwargs
        else:
            raise ValueError("Invalid arguments")

        self._is_valid = self._source.get('isValid')
        self._validation_errors = self._source.get('validationErrors')

    @property
    def is_valid(self):
        """bool: is the query valid or not?"""
        return self._is_valid

    @property
    def validation_errors(self):
        """list of errors (string) if any"""
        return self._validation_errors
