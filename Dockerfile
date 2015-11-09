FROM ubuntu:latest

RUN apt-get update && apt-get install -y python-pip

RUN pip install SPARQLWrapper

RUN pip install enum

RUN mkdir /home/dbpediaotd

ADD . /home/dbpediaotd

WORKDIR /home/dbpediaotd

CMD python DBPedia_On_This_Day.py