from flask import Flask, render_template, request, Response, jsonify
import uuid
import os
import datetime
import json
import sys

# we need this tmp 'hack' here
sys.path.append(os.path.dirname(os.path.realpath(__name__)) + '/../')

from common.database_handler import DatabaseHandler
from common.models.house_record import HouseRecord
from common.encrypt_decrypt import *

import pika
from pika.exceptions import ConnectionClosed, ChannelClosed

app = Flask(__name__)
app.debug = True

upload_folder = os.path.dirname(os.path.realpath(__name__))
app.config['upload_folder'] = upload_folder

handler = DatabaseHandler('sqlite:///house_record.db')

#users
users = ['admin', 'user', 'anna', 'jake']

# Routes
@app.route("/")
def index():
    return render_template('base.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', '')
    password = request.json.get('password', '')

    # TODO: do db query to check if credentials are correct
    # use hashlib.sha256(password).hexdigest()
    if username  == 'admin' and password == 'admin':
        response = jsonify(success=True, msg='')
        response.status_code = 200
    else:
        response = jsonify(success=False, msg='Invalid credentials')
        response.status_code = 401
    return response


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    # TODO: get username from cookie and store it as the author of record
    if file.content_type == 'text/csv':
        filename = file.filename
        try:
            file.save(os.path.join(app.config['upload_folder'], filename))
        except Exception as e:
            data = json.dumps({"message": "error when saving file on disk"})
            resp = Response(data, status=511, mimetype='application/json')
            return resp
        i = 0
        records = []
        my_csv = open(app.config['upload_folder']+"/"+filename, 'r')
        for line in my_csv.readlines():
            values = line.replace('"', "").split(',')[:11]
            if values[0] == 'id':
                continue
            h = HouseRecord()
            h.id = str(uuid.uuid4())
            h.user_id = i % len(users) + 1
            h.date_posted = datetime.datetime.strptime(values[1].split('T')[0],
                                                       "%Y%m%d").date()
            h.price = values[2]
            h.beds = values[3]
            h.baths = values[4]
            h.sqft_house = values[5]
            h.sqft_lot = values[6]
            h.floors = values[7]
            h.condition = values[10]
            i += 1
            records.append(h)

        handler.save_records(records)
        data = json.dumps({"message": "data stored"})
        resp = Response(data, status=200, mimetype='application/json')
        #send messages to rabbitmq queue
        #for record in records:
        #    message = json.dumps({"uuid": record.id, "action": "default"})

        # send messages to rabbitmq per each row saved in db

        record_ids = [r.id for r in records]

        try:
            for r_id in record_ids:
                data = {
                    "id": r_id,
                    "action": "default"
                }
                message = json.dumps(data)

                connection = pika.BlockingConnection(pika.ConnectionParameters(
                    host='localhost'))
                channel = connection.channel()

                res = channel.queue_declare(queue='task_queue', durable=True)
                channel.basic_publish(exchange='',
                                      routing_key='task_queue',
                                      body=message,
                                      properties=pika.BasicProperties(
                                          delivery_mode=2,
                                      ))
                print("Sent %r" % message)
                print 'Messages in queue %d' % res.method.message_count
                connection.close()
        except (ConnectionClosed, ChannelClosed) as e:
            print("Connecting with queue failed!")

        return resp
    else:
        data = json.dumps({"message": "Only csv is supported"})
        resp = Response(data, status=501, mimetype='application/json')
        return resp

@app.route('/viewall')
def view():
    try:
        results = handler.get_houserecords()
        houserecords = []
        for result in results:
            data ={"id":result.id,
                   "date_posted": str(result.date_posted),
                   "price": result.price,
                   "beds": result.beds,
                   "baths": result.baths,
                   "sqft_house": result.sqft_house,
                   "sqft_lot": result.sqft_lot,
                   "floors": result.floors,
                       "condition": result.condition}
            houserecords.append(data)
        data = json.dumps({"message": houserecords})
        resp = Response(data, status=200, mimetype='application/json')
        return resp
    except Exception as e:
        print e
        resp = Response(status=500)
        return resp


@app.route('/results/<username>')
def get_results(username="admin"):
    try:
        bare_results = handler.get_data_for_user(username)
        results = [{"action": r.action, "result": decrypt(r.result)} for r in bare_results]
        resp = Response(json.dumps(results), status=200, mimetype='application/json')
    except Exception as e:
        print e
        resp = Response(status=500, response=str(e))
    return resp


def decrypt(cipher_text):
    try:
        plain = decrypt_fernet(cipher_text)
    except Exception as e:
        #means we're running locally
        plain = cipher_text
    finally:
        return cipher_text

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8181, debug=True)
