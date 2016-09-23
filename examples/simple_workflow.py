from __future__ import print_function

from smartobjects import SmartObjectsClient, Environments
from smartobjects.restitution.search import ResultSet

CLIENT_ID = "<CLIENT_ID>"
CLIENT_SECRET = "<CLIENT_SECRET>"


def main():
    # initialize the client with your client_id and client_secret
    # (available in the "API Credential" section of your dashboard)
    client = SmartObjectsClient(CLIENT_ID, CLIENT_SECRET, Environments.Production)

    # use the OwnersService to find if an owner already exists or to create it
    if not client.owners.owner_exists("support@mnubo.com"):
        owner = {
            "username": "support@mnubo.com",
            "x_password": "owner_password",
            "zip_code": "H3K 1G6"
        }
        client.owners.create(owner)

    # use the ObjectsService to find if an object already exists or to create it
    if not client.objects.object_exists("cat_detector_kitchen"):
        smartobject = {
            "x_device_id": "cat_detector_kitchen",
            "x_object_type": "cat_detector",
            "model": "pro"
        }
        client.objects.create(smartobject)

        # link an object to an owner with "claim"
        client.owners.claim("support@mnubo.com", "cat_detector_kitchen")

    # use the EventsService to publish new events
    # events can be sent by batches of up to 1000 events
    events = [
        {"x_event_type": "cat_detected", "type": "soft", "speed": i}
        for i in range(10)
    ]
    event_results = client.events.send_from_device("cat_detector_kitchen", events)

    # make sure every event was accepted
    failed = filter(lambda r: r.result != "success", event_results)
    for f in failed:
        print("- {id}: {reason}".format(id=f.id, reason=f.message))

    # it is recommended to validate your complex queries with this special endpoints to ease development
    # and reduce errors
    query = {
        "from": "event",
        "where": {
            "and": [
                {"speed": {"eq": 0}},
                {"x_timestamp": {"dateBetween": "2016-08-22", "and": "2016-08-27"}
                 }
            ]
        },
        "select": [
            {"value": "version"},
            {"value": "time_created"}
        ]
    }

    validation_result = client.search.validate_query(query)

    if not validation_result.is_valid:
        print(validation_result.validation_errors)
    else:
        # search for events with the search API
        # note: events submitted above might not be immediately available for querying as they must be fully
        #   processed by the SmartObjects platform
        resultset = client.search.search(query)
        print("We got {} results:".format(len(resultset)))
        for row in resultset:
            print("version: {}, created: {}".format(row.get("version"), row.get("time_created", ResultSet.ToDatetime)))

    # explore properties of the datamodel with search.get_datasets
    # https://sop.mtl.mnubo.com/apps/doc/api.html#get-api-v3-search-datasets
    datasets = client.search.get_datasets()
    for owner_field in datasets["event"].fields:
        if not owner_field.key.startswith("x_"):
            print("{0} ({1}): {2}".format(owner_field.key, owner_field.high_level_type, owner_field.description))


if __name__ == "__main__":
    main()
