#!/usr/bin/env python

from setuptools import setup
from mnubo import __version__, __author__, __email__

with open('requirements.txt') as f:
    requirements = [line.strip() for line in f.readlines()]

setup(
    name="mnubo",
    version=__version__,
    description="Python client to access mnubo ingestion and restitution APIs",
    author=__author__,
    author_email=__email__,
    url="https://github.com/mnubo/smartobjects-python-client",
    packages=["mnubo"],
    install_requires=requirements,
    keywords=['mnubo', 'api', 'sdk', 'iot', 'smartobject'],
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)