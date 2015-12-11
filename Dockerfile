FROM python:latest

RUN pip install sparqlwrapper

RUN mkdir /home/dbpediaotd

ADD . /home/dbpediaotd

WORKDIR /home/dbpediaotd

