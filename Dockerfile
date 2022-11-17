FROM python:3.10

RUN apt-get update -y && apt-get upgrade -y

WORKDIR /aiogram_template
COPY . .

RUN pip install -r requirements.txt