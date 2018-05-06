FROM python:3.5-slim

RUN apt-get update \
  && apt-get upgrade -yqq \
  && apt-get install -yqq build-essential libmysqlclient-dev mysql-client

COPY ./requirements.txt /root/requirements.txt
RUN pip install -r /root/requirements.txt \
  && pip install tox ipython python-decouple dj-database-url mysqlclient

COPY . /opt/project
RUN cd /opt/project/ \
  && pip install -e .

WORKDIR /opt/project/example/
EXPOSE 8000
CMD ./manage.py runserver 0.0.0.0:8000
