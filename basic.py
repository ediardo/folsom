from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import house_record

app = Flask(__name__)

engine = create_engine('sqlite:///house_record.db')
house_record.Base.metadata = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def index():
    return "OSIC Hackathon Application"

@app.route('/houses')
def displayAll():
    houses = session.query(house_record.HouseRecord)
    return render_template('allhouserecords.html', houses=houses)

@app.route('/process', methods=["POST"])
def processInput():
    pass
    # request.headers #check if file
    # request.files #read attached files
    # #parsing
    # #save in database
    # #get indexes of saved rows
    # #create messages for each row
    # #send msg when ready
