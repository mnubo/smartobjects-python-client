FROM python:3.6.8-slim-jessie

ENV SHELL /bin/bash

RUN pip install pylint autopep8 rope

ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
