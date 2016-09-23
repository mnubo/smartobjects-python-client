#!/usr/bin/env python

from setuptools import setup

with open('requirements.txt') as f:
    requirements = [line.strip() for line in f.readlines()]

VERSION = "1.0{tag}"
try:
    with open('build_version.txt') as f:
        tag = f.readline().strip()
        version = VERSION.format(tag="."+tag)
except IOError:
    version = VERSION.format(tag="-dev")

setup(
    name="smartobjects",
    version=version,
    description="Python client to access mnubo's SmartObjects ingestion and restitution APIs",
    author="mnubo, inc.",
    author_email="support@mnubo.com",
    url="https://github.com/mnubo/smartobjects-python-client",
    packages=["smartobjects", "smartobjects.ingestion", "smartobjects.restitution"],
    install_requires=requirements,
    keywords=['mnubo', 'api', 'sdk', 'iot', 'smartobjects'],
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
