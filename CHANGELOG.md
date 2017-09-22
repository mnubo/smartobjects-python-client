<a name='1.2.1'></a>

# [1.2.1](https://github.com/mnubo/smartobjects-python-client/compare/1.0.37...1.2.1) (2017-09-22)


* Support initialization with a custom url
<a name='1.0.37'></a>

# [1.0.37](https://github.com/mnubo/smartobjects-python-client/compare/1.2.0...1.0.37) (2017-09-22)


* Support initialization with a custom url
<a name='1.2.0'></a>

# [1.2.0](https://github.com/mnubo/smartobjects-python-client/compare/1.1.1...1.2.0) (2017-08-18)


* Support initialization with a static access token
<a name='1.1.1'></a>

# [1.1.1](https://github.com/mnubo/smartobjects-python-client/compare/1.1.0...1.1.1) (2017-08-16)


* Support for python3
<a name='1.1.0'></a>

# [1.1.0](https://github.com/mnubo/smartobjects-python-client/compare/1.0.36...1.1.0) (2017-07-11)


- Opt in exponential backoff for responses with 503 status code
<a name='1.0.36'></a>

# [1.0.36](https://github.com/mnubo/smartobjects-python-client/compare/1.0.35...1.0.36) (2017-05-09)


- Bugfixes with dataframe
<a name='1.0.35'></a>

# [1.0.35](https://github.com/mnubo/smartobjects-python-client/compare/1.0.34...1.0.35) (2017-05-09)


- Added support for dataframe if pandas is installed
<a name='1.0.34'></a>

# [1.0.34](https://github.com/mnubo/smartobjects-python-client/compare/1.0.33...1.0.34) (2017-04-26)


- Added origin to EventType
<a name='1.0.33'></a>

# [1.0.33](https://github.com/mnubo/smartobjects-python-client/compare/1.0.32...1.0.33) (2017-04-25)


- Added support for a body on claim/unclaim
<a name='1.0.32'></a>

# [1.0.32](https://github.com/mnubo/smartobjects-python-client/compare/1.0.31...1.0.32) (2017-04-24)


Fix packaging options to expose smartobjects.model
<a name='1.0.31'></a>

# [1.0.31](https://github.com/mnubo/smartobjects-python-client/compare/1.0.30...1.0.31) (2017-04-24)


- Added model service to get the data model

The model exposes all of the following:

- Event types
- Timeseries
- Object types
- Object attributes
- Owner attributes
- Sessionizers

The returned model contains everything that is applied the zone (sandbox or production) your are currently working with. By definition, everything that is available in the production view is also available in the sandbox view. The opposite is not true.
<a name='1.0.30'></a>

# [1.0.30](https://github.com/mnubo/smartobjects-python-client/compare/1.0.29...1.0.30) (2017-03-24)


- Added batch_claim and batch_unclaim to the "owners" service
- Fixed doc links
<a name='1.0.29'></a>

# [1.0.29](https://github.com/mnubo/smartobjects-python-client/compare/1.0.28...1.0.29) (2017-01-31)


### Helpers

* fixing import of helpers which resulted in being unresolved.
<a name='1.0.28'></a>

# [1.0.28](https://github.com/mnubo/smartobjects-python-client/compare/1.0.26...1.0.28) (2017-01-12)


### Helpers

* added helpers to build the JSON expected by ingestion
<a name='1.0.26'></a>

# [1.0.26](https://github.com/mnubo/smartobjects-python-client/compare/1.0.25...1.0.26) (2016-11-30)


### Features

* **POST /api/v3/owners/{username}/objects/{device}/unclaim**: support for unclaim object
