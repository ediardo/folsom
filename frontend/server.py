from flask import Flask, render_template, send_file, request, Response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.house_record import Base
import uuid
import os
import datetime
import json
from models.house_record import HouseRecord

app = Flask(__name__)
app.debug = True
upload_folder = '/opt/stack/new/folsom'
app.config['upload_folder'] = upload_folder

engine = create_engine('sqlite:///house_record.db', echo=True)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)


# Routes

@app.route("/")
def index():
    return render_template('base.html')

@app.route('/login')
# GET renders HTML login form
def login():
    # aradhana
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

        records = []
        session = DBSession()
        my_csv = open(app.config['upload_folder']+"/"+filename, 'r')
        for line in my_csv.readlines():
            values = line.replace('"', "").split(',')[:11]
            if values[0] == 'id':
                continue
            h = HouseRecord()
            h.id = str(uuid.uuid4())
            h.date_posted = datetime.datetime.strptime(values[1].split('T')[0],
                                                       "%Y%m%d").date()
            h.price = values[2]
            h.beds = values[3]
            h.baths = values[4]
            h.sqft_house = values[5]
            h.sqft_lot = values[6]
            h.floors = values[7]
            h.condition = values[10]
            session.add(h)
            session.commit()

            records.append(h)

        # send messages to rabbitmq queue
        #for record in records:
        #    data = json.dumps({"uuid": record.id})

        #check to if data has been stored
        session = DBSession()
        results = session.query(HouseRecord)
        for result in results:
            print result.price

        data = json.dumps({"message": "data stored"})
        resp = Response(data, status=200, mimetype='application/json')
        return resp

    else:
        data = json.dumps({"message": "Only csv is supported"})
        resp = Response(data, status=501, mimetype='application/json')
        return resp

if __name__ == "__main__":
    app.run(host='192.168.33.12', port=8181, debug=True)
