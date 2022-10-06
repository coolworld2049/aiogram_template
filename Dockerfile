FROM ubuntu:22.04
LABEL "aiogram_template"="coolworld2049" maintainer="coolworld2049@gmail.com"

ARG _PROJECT_NAME='aiogram_template'
ARG _PROJECT_USER='testbot'
ARG _DB_NAME='testbot'
ARG _PGUSER='postgres'
ARG _PGPASS='qwerty'
ARG _TZ='Europe/Mocsow'

ARG DEBIAN_FRONTEND=noninteractive

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

RUN useradd -ms /bin/bash $PROJECT_USER && \
    usermod -aG sudo $PROJECT_USER
    
RUN apt update && apt upgrade && \
    apt --assume-yes install python3 && \
    apt --assume-yes install python3-venv && \
    apt --assume-yes install python3-pip && \
    apt --assume-yes install postgresql postgresql-contrib && \
    apt --assume-yes install redis

USER $PROJECT_USER


RUN sudo mkdir -p /var/$PROJECT_USER/$PROJECT_NAME && \
    sudo chown -R $PROJECT_USER /var/$PROJECT_NAME/

WORKDIR /var/$PROJECT_USER/$PROJECT_NAME

RUN pip install -r requirements.txt

COPY . /var/$PROJECT_USER/$PROJECT_NAME/
COPY /etc/systemd/system/ /var/$PROJECT_USER/$PROJECT_NAME/$PROJECT_NAME.service
COPY /tmp/ /var/$PROJECT_USER/$PROJECT_NAME/database/schema.sql


USER postgres

RUN systemctl start postgresql.service && \
    sudo -i -u postgres && \
    createdb $DB_NAME && \
    psql -d $DB_NAME -c "CREATE schema schema;" && \
    psql -d $DB_NAME -c "SET schema 'schema';" && \
    psql -d $DB_NAME -c "ALTER USER $PGUSER PASSWORD $PGUSER;" && \
    psql -d $DB_NAME -a -q -f /tmp/schema.sql && \
    exit && clear \


USER $PROJECT_USER

CMD systemctl daemon-reload && \
    systemctl enable $PROJECT_NAME.service && \
    systemctl start $PROJECT_NAME.service && \
    systemctl status $PROJECT_NAME.service