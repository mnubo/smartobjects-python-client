#!/usr/bin/env python

from setuptools import setup

setup(
    name="mnubo-sdk",
    version="0.0.1",
    description="Python SDK to access mnubo ingestion APIs",
    author="mnubo",
    author_email="sos@mnubo.com",
    url="https://github.com/mnubo/mnubo-python-sdk",
    packages=["mnubo-sdk"],
    install_requires=['requests>=2.5,<3.0'],
    tests_require=['nose', 'mock'],
    keywords = ['mnubo', 'api', 'sdk', 'iot', 'smartobject']
)