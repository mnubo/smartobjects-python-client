#!/usr/bin/env python

from setuptools import setup

with open('requirements.txt') as f:
    requirements = [line.strip() for line in f.readlines()]

VERSION = "2.0{tag}"
try:
    with open('build_version.txt') as f:
        tag = f.readline().strip()
        version = VERSION.format(tag="."+tag)
except IOError:
    version = VERSION.format(tag="-dev")

setup(
    name="mnubo",
    version=version,
    description="Python client to access mnubo SmartObjects ingestion and restitution APIs",
    author="mnubo, inc.",
    author_email="support@mnubo.com",
    url="https://github.com/mnubo/smartobjects-python-client",
    packages=["mnubo", "mnubo.ingestion", "mnubo.restitution"],
    install_requires=requirements,
    keywords=['mnubo', 'api', 'sdk', 'iot', 'smartobject'],
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
