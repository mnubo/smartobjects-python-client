from smartobjects.model import Model

class ModelService(object):
    def __init__(self, api_manager):
        """ Initializes SearchServices with the api manager
        """

        self.api_manager = api_manager

    def export(self):
        """ Export the model in the current environment 

        see https://smartobjects.mnubo.com/apps/doc/api_model.html for more details.
        :returns: Model

        Example:
        >>> model = client.model.fetch()
        >>> for obj in value.object_attributes:
        >>>        print(obj.key)
        >>>        print(obj.description)
        """
        return Model(self.api_manager.get('model/export').json())