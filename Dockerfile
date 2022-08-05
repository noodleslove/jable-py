FROM python:3.10-slim-buster

RUN apt-get update && apt-get -y install cron vim

WORKDIR /jable-py

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN chmod 0644 ./crontab
RUN crontab ./crontab

CMD ["cron", "-f"]
