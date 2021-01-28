from smartobjects import SmartObjectsClient, Environments
from smartobjects.model import Model, Timeseries, ObjectAttribute, OwnerAttribute, EventType, ObjectType

CLIENT_ID = "<CLIENT_ID>"
CLIENT_SECRET = "<CLIENT_SECRET>"


# This workflow create/deploy attributes. These operations are limited to the
# sandbox environment.
def main():
    # initialize the client with your client_id and client_secret
    client = SmartObjectsClient(CLIENT_ID, CLIENT_SECRET, Environments.Sandbox)

    # create an object type
    client.model.sandbox_ops.object_types_ops.createOne({
        'key': 'cat_detector',
        'description': '',
        'objectAttributesKeys': []
    })
    # create an object attribute bound to the object type above
    client.model.sandbox_ops.object_attributes_ops.createOne({
        'key': 'model',
        'displayName': 'Model',
        'description': 'model of the cat detector',
        'type': {
            'containerType': 'none',
            'highLevelType': 'TEXT'
        },
        'objectTypeKeys': ['cat_detector']
    })

    # create an event type
    client.model.sandbox_ops.event_types_ops.createOne({
        'key': 'cat_detected',
        'origin': 'unscheduled',
        'description': 'events triggered when a cat is detected',
        'timeseriesKeys': []
    })
    # create a few timeseries and bind them to the event type above
    client.model.sandbox_ops.timeseries_ops.createOne({
        'key': 'speed',
        'displayName': 'Speed (m/s)',
        'description': 'Speed of the cat',
        'type': {
            'highLevelType': 'DOUBLE'
        },
        'eventTypeKeys': ['cat_detected']
    })
    client.model.sandbox_ops.timeseries_ops.createOne({
        'key': 'version',
        'displayName': 'Version',
        'description': 'Version of the detector',
        'type': {
            'highLevelType': 'TEXT'
        },
        'eventTypeKeys': ['cat_detected']
    })

    # create an owner attribute
    owner = OwnerAttribute({
        'key': 'zip_code',
        'displayName': 'Zip Code',
        'description': 'Zip code of the owner of the detector',
        'type': {
            'containerType': 'none',
            'highLevelType': 'TEXT'
        }
    })
    client.model.sandbox_ops.owner_attributes_ops.createOne(owner)

    # deploy the entities in production
    client.model.sandbox_ops.timeseries_ops.deploy('speed')
    client.model.sandbox_ops.timeseries_ops.deploy('version')
    client.model.sandbox_ops.object_attributes_ops.deploy('model')
    client.model.sandbox_ops.owner_attributes_ops.deploy(owner.key)

    model = client.model.export()
    print("Number of event types - {}".format(len(model.event_types)))
    print("Number of timeseries - {}".format(len(model.timeseries)))
    print("Number of object types - {}".format(len(model.object_types)))
    print("Number of object attributes - {}".format(len(model.object_attributes)))

if __name__ == "__main__":
    main()
