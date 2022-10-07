FROM ubuntu:22.04
LABEL "aiogram_template"="coolworld2049" maintainer="coolworld2049@gmail.com"

ARG _PROJECT_NAME='aiogram_bot_template'
ARG _PROJECT_USER='testbot'
ARG _DB_NAME='testbot'
ARG _PGUSER='postgres'
ARG _PGPASS='qwerty'
ARG _TZ='Europe/Moscow'
ARG DEBIAN_FRONTEND_nonintv='noninteractive'
ARG DEBIAN_FRONTEND_intv='interactive'

ENV PROJECT_NAME $_PROJECT_NAME
ENV PROJECT_USER $_PROJECT_USER
ENV DB_NAME $_DB_NAME
ENV PGUSER $_PGUSER
ENV PGPASS $_PGPASS
ENV TZ $_TZ

RUN echo $PROJECT_NAME
RUN echo $PROJECT_USER
RUN echo $DB_NAME
RUN echo $PGUSER
RUN echo $PGPASS


USER root

COPY . /$PROJECT_NAME/

RUN useradd -ms /bin/bash $PROJECT_USER && usermod -aG sudo $PROJECT_USER

RUN apt update && apt upgrade

ENV DEBIAN_FRONTEND $DEBIAN_FRONTEND_nonintv
RUN apt --assume-yes install postgresql postgresql-contrib
ENV DEBIAN_FRONTEND $DEBIAN_FRONTEND_intv

RUN apt --assume-yes install python3 && \
    apt --assume-yes install python3-venv && \
    apt --assume-yes install python3-pip && \
    apt --assume-yes install redis


USER $PROJECT_USER

RUN echo PROJECT_USER

WORKDIR /$PROJECT_NAME/
RUN pip install -r requirements.txt


USER root

RUN -i -u postgres
RUN createdb $DB_NAME
RUN psql -d $DB_NAME -c "CREATE schema schema;"
RUN psql -d $DB_NAME -c "SET schema 'schema';"
RUN psql -d $DB_NAME -c "ALTER USER $PGUSER PASSWORD '$PGUSER';" \
RUN psql -d $DB_NAME -f /$PROJECT_NAME/schema.sql


USER $PROJECT_USER
RUN echo $PROJECT_USER

CMD systemctl daemon-reload && \
    systemctl enable $PROJECT_NAME.service && \
    systemctl start $PROJECT_NAME.service && \
    systemctl status $PROJECT_NAME.service