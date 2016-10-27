from flask import Flask, render_template, request, Response
import uuid
import os
import datetime
import json

from database.database_handler import DatabaseHandler
from database.models.house_record import HouseRecord

app = Flask(__name__)
app.debug = True

upload_folder = '/opt/stack/folsom'
app.config['upload_folder'] = upload_folder

handler = DatabaseHandler('sqlite:///house_record.db')

#users
users = ['admin', 'user', 'anna', 'jake']

# Routes
@app.route("/")
def index():
    return render_template('base.html')

@app.route('/login')
# GET renders HTML login form
def login():
    return render_template('partials/login.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['csv']
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
        resp = Response( status=500)
        return resp

if __name__ == "__main__":
    app.run(host='192.168.33.12', port=8181, debug=True)
