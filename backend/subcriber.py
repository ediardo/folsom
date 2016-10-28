import time
import pika
import json
from daemon import runner
from database.database_handler import DatabaseHandler
from database.models.house_record import HouseRecord
from process_data import process_record

class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/foo.pid'
        self.pidfile_timeout = 5
	#chagne this connection string to the remote sql connection once we have containers
	self.handler = DatabaseHandler('sqlite:///house_record.db')

    def do_work(self, channel):
            print('Waiting for messages. To exit press CTRL+C')

            def callback(ch, method, properties, body):
                data = json.loads(body)
		id = data['id']
                print id
		record = self.handler.get_record_by_id(id)
		results = process_record("default", record)
		self.handler.save_result(results[1], results[0])
                ch.basic_ack(delivery_tag = method.delivery_tag)

            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(callback,queue='task_queue')
            channel.start_consuming()

    def run(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='task_queue', durable=True)

        while True:
            self.do_work(channel)
            #sleep?

app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()

