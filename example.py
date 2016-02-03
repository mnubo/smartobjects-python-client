import json
import mnubo.api_manager
import mnubo.services
from mnubo.mnubo_client import MnuboClient

mnubo = MnuboClient('<your_client_id>', '<your_client_secret>', 'https://rest.sandbox.mnubo.com')

################
# Create an Object
################

Obj={}
Obj["x_device_id"]="object-test"
Obj["x_object_type"]="thermostat"
Obj["x_registration_date"]="2015-01-01T12:00:00"
Obj["x_registration_latitude"]=66.983
Obj["x_registration_longitude"]=-160.433
Obj["account_id"]=362
Obj["ip_address"]="24.225.187.170"
Obj=json.dumps(Obj)

response = mnubo.smart_object_services.create(Obj)
if response.status_code == 201:
    print "Object Create SUCCEEDED"   
else:
    print "Object Create FAILED"
    r = json.loads(response.content)
    print r["message"]

################
# Update an Object
################

Obj={}
Obj["x_device_id"]="object-test"
Obj["account_id"]= 366
Obj["ip_address"]="24.225.127.70"

response = mnubo.smart_object_services.update(Obj)
if response.status_code == 200:
    print "Object Update SUCCEEDED"   
else:
    print "Object Update FAILED"
    r = json.loads(response.content)
    print r["message"]

################
# Create an Owner
################

Owner={}
Owner["username"]="owner-test"
Owner["x_password"]="12345678"
Owner["x_registration_date"]="2015-01-01T12:00:00"
Owner=json.dumps(Owner)

response = mnubo.owner_services.create(Owner)
if response.status_code == 201:
    print "Owner Create SUCCEEDED"   
else:
    print "Owner Create FAILED"
    r = json.loads(response.content)
    print r["message"]

################
# Update an Owner
################

Owner={}
Owner["username"]="owner-test"
Owner["x_password"]="12345678"
Owner["x_registration_date"]="2014-02-01T12:00:00"

response = mnubo.owner_services.update(Owner)
if response.status_code == 200:
    print "Owner Update SUCCEEDED"   
else:
    print "Owner Update FAILED"
    r = json.loads(response.content)
    print r["message"]

################
# Claim Object
################
response = mnubo.owner_services.claim('owner-test', 'object-test')
if response.status_code == 200:
    print "Claim Object SUCCEEDED"   
else:
    print "Claim Object FAILED"
    r = json.loads(response.content)
    print r["message"]

################
# Post an Event
################

dev_id={}
dev_id["x_device_id"]="object-test"

Event = [{}]
Event[0]={}
Event[0]["x_object"]=dev_id
Event[0]["x_event_type"]= "thermostat_measurement"
Event[0]["x_latitude"]=66.983
Event[0]["x_longitude"]=-160.433
Event[0]["ampere"]=0.3
Event[0]["temperature"]=23
Event[0]["humidity"]=80
Event[0]["watt_hour"]=12
Event=json.dumps(Event)

response = mnubo.event_services.send(Event)
if response.status_code == 200:
    print "Post Event SUCCEEDED"   
else:
    print "Post Event FAILED"
    r = json.loads(response.content)
    print r["message"]

################
# Delete an Object
################
response = mnubo.smart_object_services.delete('object-test')
if response.status_code == 200:
    print "Object DELETED"   
else:
    print "Delete Object FAILED"
    r = json.loads(response.content)
    print r["message"]
    
################
# Delete an Owner
################

response = mnubo.owner_services.delete('owner-test')
if response.status_code == 200:
    print "Owner DELETED"   
else:
    print "Delete Owner FAILED"
    r = json.loads(response.content)
    print r["message"]