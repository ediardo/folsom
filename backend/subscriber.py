import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__name__)) + '/../')
import pika
import json
from common.database_handler import DatabaseHandler
from common.encrypt_decrypt import *
from process_data import process_record

class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/foo.pid'
        self.pidfile_timeout = 5
        self.mq_host = os.getenv("MQ_HOST") or 'localhost'
        self.mq_port = os.getenv("MQ_PORT") or 5672
        # chagne this connection string to the remote sql connection once we have containers
        self.handler = DatabaseHandler('sqlite:///house_record.db')

    def do_work(self, channel):
        print('Waiting for messages on host ' + self.mq_host + \
              ':' + str(self.mq_port) + '. To exit press CTRL+C')

        def callback(ch, method, properties, body):
            data = json.loads(body)
            id = data['id']
            print id
            record = self.handler.get_record_by_id(id)
            results = process_record(data["action"], record)
            self.handler.save_result(results[0], encrypt_fernet(results[1]) , action=data["action"])
            ch.basic_ack(delivery_tag = method.delivery_tag)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(callback,queue='task_queue')
        channel.start_consuming()

    def run(self):
        if not self.mq_host or not self.mq_port:
            self.mq_host = 'localhost'
            self.mq_port = 5672
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                                                         host=self.mq_host,
                                                         port=int(self.mq_port)))
        channel = connection.channel()
        channel.queue_declare(queue='task_queue', durable=True)

        while True:
            self.do_work(channel)
            #sleep?

app = App()
app.run()

