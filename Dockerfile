FROM debian:jessie
MAINTAINER Joanna Taryma "joanna.r.taryma@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential libssl-dev libyaml-dev libpython2.7-dev

COPY backend /app/backend
COPY database /app/database
WORKDIR /app/backend
RUN pip install -r requirements.txt

ENV MQ_HOST=192.168.30.3
ENV MQ_PORT=5672
ENTRYPOINT ["python", "subscriber.py"]
#CMD ["ls"]
CMD ["start"]
