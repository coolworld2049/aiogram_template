FROM python:3.10.7

RUN apt-get update -y && apt-get upgrade -y && apt install git -y

WORKDIR /app
RUN git clone https://github.com/coolworld2049/aiogram_template.git /app/aiogram_template

WORKDIR /app/aiogram_template
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "app.py"]