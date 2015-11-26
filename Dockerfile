FROM ubuntu:latest

RUN apt-get update && apt-get install -y python-pip

RUN pip install SPARQLWrapper

RUN pip install enum

RUN pip install simplejson

RUN mkdir /home/dbpediaotd

ADD . /home/dbpediaotd

WORKDIR /home/dbpediaotd

RUN python DBPedia_On_This_Day.py 
