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


---
#<a name="section3"></a>3. Pre-requisites

- Python 2.7


---
#<a name="section4"></a>4. Installation & Configuration

    pip install mnuboSDK
    
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

```python
response = mnubo.owner_services.create(new_owner)
```

### Use the Smart Objects Services
To create smart objects on the mnubo SmartObject platform, please refer to 
the data modeling guide to format correctly the smart object's data structure.

```python
response = mnubo.smart_object_services.create(new_object)
```

### Use the Event Services
To send events to the mnubo SmartObject platform, please refer to 
the data modeling guide to format correctly the event's data structure.

```python
response = mnubo.event_services.send(event)
```

---
#<a name="section6"></a>6. Important notes



---
#<a name="section7"></a>7. Source code



---
#<a name="section8"></a>8. Known limitations



---
#<a name="section9"></a>9. References

