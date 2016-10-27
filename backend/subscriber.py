import time
import os
import pika
import json

class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/foo.pid'
        self.pidfile_timeout = 5
        self.mq_host = os.getenv("MQ_HOST") or 'localhost'
        self.mq_port = os.getenv("MQ_PORT") or 5672

    def do_work(self, channel):
            print('Waiting for messages on host ' + self.mq_host + \
                  ':' + str(self.mq_port) + '. To exit press CTRL+C')

            def callback(ch, method, properties, body):
                data = json.loads(body)
                print(data['id'])
                ch.basic_ack(delivery_tag = method.delivery_tag)

            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(callback,
                      queue='task_queue')

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
