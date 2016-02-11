# mnubo Python SDK

Table of Content
================

[1. Introduction](#section1)

[2. Architecture](#section2)

[3. Pre-requisites](#section3)

[4. Installation & Configuration](#section4)

[5. Usage](#section5)

[6. Important notes](#section6)

[7. Source code](#section7)

[8. Known limitations](#section8)

[9. References](#section9)

---
#<a name="section1"></a>1. Introduction

To connect your Python application to our API use the mnubo Python SDK.

---
#<a name="section3"></a>2. Architecture


* `OwnerServices`
  - `create`
  - `claim`
  - `update`
  - `delete`

* `ObjectServices`
  - `create`
  - `update`
  - `delete`

* `EventServices`
  - `send`
  
* `SearchServices`
  - `search`
  - `search_datasets`


---
#<a name="section3"></a>3. Pre-requisites

- Python 2.7


---
#<a name="section4"></a>4. Installation & Configuration

    pip install mnubo

---
#<a name="section5"></a>5. Usage

### Initialize the MnuboClient

```python
from mnubo.mnubo_client import MnuboClient

mnubo = MnuboClient('CLIENT_ID', 'CLIENT_SECRET', 'HOSTNAME')
```

### Use the Owner Services
To create owners on the mnubo SmartObject platform, please refer to
the data modeling guide to format correctly the owner's data structure.

#### Create an Owner
```python
response = mnubo.owner_services.create('OWNER_IN_JSON')
```

#### Claim a Smart Object for an Owner
```python
response = mnubo.owner_services.claim('USERNAME', 'DEVICE_ID')
```

#### Update an Owner
```python
response = mnubo.owner_services.update('OWNER_IN_JSON')
```

#### Delete an Owner
```python
response = mnubo.owner_services.delete('USERNAME')
```

### Use the Smart Objects Services
To create smart objects on the mnubo SmartObject platform, please refer to
the data modeling guide to format correctly the smart object's data structure.

#### Create a Smart Object
```python
response = mnubo.smart_object_services.create('OBJECT_IN_JSON')
```

#### Update a Smart Object
```python
response = mnubo.smart_object_services.update('OBJECT_IN_JSON')
```

#### Delete a Smart Object
```python
response = mnubo.smart_object_services.delete('DEVICE_ID')
```

### Use the Event Services
To send events to the mnubo SmartObject platform, please refer to
the data modeling guide to format correctly the event's data structure.

#### Send an Event
```python
response = mnubo.event_services.send('EVENT_IN_JSON')
```

### Use the Search Services
To send search queries to the mnubo SmartObject platform, please refer to
the Search API documentation to format your queries correctly.

#### Search Query
```python
response = mnubo.search_services.search('QUERY')
```

#### Search Datasets Query
```python
response = mnubo.search_services.search_datasets('QUERY')
```

---
#<a name="section6"></a>6. Important notes



---
#<a name="section7"></a>7. Source code



---
#<a name="section8"></a>8. Known limitations



---
#<a name="section9"></a>9. References
