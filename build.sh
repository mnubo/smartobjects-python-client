#!/bin/bash

if [ "$TRAVIS_PULL_REQUEST" = "false" ]; then
    openssl aes-256-cbc -K $encrypted_61cb1dc33abe_key -iv $encrypted_61cb1dc33abe_iv \
    	-in creds.ini.enc -out ittests/resources/creds.ini -d
    python -m unittest discover -v tests/ && python -m unittest discover -v ittests/
else
    python -m unittest discover -v tests/
fi