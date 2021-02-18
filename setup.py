#!/usr/bin/env python

import os

here = os.path.abspath(os.path.dirname(__file__))

from setuptools import setup

versiondict = {}
try:
    with open(os.path.join(here, 'smartobjects', '__version__.py'), mode='r') as f:
        exec(f.read(), versiondict)
except IOError:
    versiondict['__version__'] = 'dev'

with open('requirements.txt') as f:
    requirements = [line.strip() for line in f.readlines()]

setup(
    name="smartobjects",
    version=versiondict['__version__'],
    description="Python client to access mnubo's SmartObjects ingestion and restitution APIs",
    author="mnubo, inc.",
    author_email="support@mnubo.com",
    url="https://github.com/mnubo/smartobjects-python-client",
    packages=["smartobjects", "smartobjects.ingestion", "smartobjects.restitution", "smartobjects.helpers",
              "smartobjects.model", "smartobjects.datalake"],
    install_requires=requirements,
    extras_require={
        "pandas": ["pandas"]
    },
    keywords=['mnubo', 'api', 'sdk', 'iot', 'smartobjects'],
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
