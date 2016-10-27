#!/bin/bash

#install requirements
sudo apt-get install python-pip -y
sudo pip install pika
sudo pip install sqlalchemy
sudo apt-get install rabbitmq-server -y

export PYTHONPATH=$PYTHONPATH:.
#test
cd frontend/
python test.py 
