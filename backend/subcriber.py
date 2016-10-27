import time
import pika
import json
from daemon import runner

class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/foo.pid'
        self.pidfile_timeout = 5
    def do_work(self, channel):
            print('Waiting for messages. To exit press CTRL+C')

            def callback(ch, method, properties, body):
                data = json.loads(body)
                print(data['id'])
                ch.basic_ack(delivery_tag = method.delivery_tag)

            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(callback,
                      queue='task_queue')

            channel.start_consuming()
    def run(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                                                         host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='task_queue', durable=True)

        while True:
            self.do_work(channel)
            #sleep?

app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()
