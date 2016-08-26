from datetime import datetime


class ResultSet(object):
    def __init__(self, *args, **kwargs):
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
        if not 0 <= item < len(self._rows):
            raise IndexError("Invalid index: must be in the range [{}, {})".format(0, len(self._rows)))
        return ResultRow(self._rows[item], self)

    def get_column_index(self, item):
        if item not in self._col_to_idx:
            raise IndexError("Invalid column '{}'".format(item))
        return self._col_to_idx[item]

    @property
    def raw(self):
        return self._source

    @property
    def columns(self):
        return self._columns

    @property
    def rows(self):
        return self._rows

    # type conversion utils
    @staticmethod
    def ToDatetime(date): return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")


class ResultRow(object):
    def __init__(self, row, parent_rs):
        self._source = row
        self._parent = parent_rs

    def __getitem__(self, item):
        return self.get(item)

    def get(self, item, rtype=None):
        if isinstance(item, str):
            index = self._parent.get_column_index(item)
        elif isinstance(item, int):
            index = item
        else:
            raise ValueError("Invalid type for argument 'item'")

        if not 0 <= index < len(self._source):
            raise IndexError("Invalid index: must be in the range [{}, {})".format(0, len(self._source)))

        if rtype:
            return rtype(self._source[index])
        else:
            return self._source[index]

    @property
    def raw(self):
        return self._source


class DataSet(object):
    """
    https://sop.mtl.mnubo.com/apps/doc/api.html#get-api-v3-search-datasets
    """
    def __init__(self, json):
        self._source = json
        self.key = self._source.get('key')
        self.description = self._source.get('key')
        self.display_name = self._source.get('displayName')
        self.fields = [Field(field) for field in self._source.get('fields', [])]


class Field(object):
    """
    https://sop.mtl.mnubo.com/apps/doc/api.html#get-api-v3-search-datasets
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
        return self._is_valid

    @property
    def validation_errors(self):
        return self._validation_errors
