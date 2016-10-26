from flask import Flask, render_template, send_file, request, Response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.house_record import Base
import uuid
from models.house_record import HouseRecord
app = Flask(__name__)
app.debug = True

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
    file = request.files['file']
    if file['csv'] == 'text/csv':
        filename = file['filename']
        my_csv = open(filename, 'r')
        records = []
        session = DBSession()
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


        print filename

        print("csv file")

    else:
        return "not csv file"

if __name__ == "__main__":
    app.run(host='192.168.33.12', port=8181, debug=True)
