#create new flask application with db connection to postgres
import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from dataclasses import dataclass
#from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:eqiQSWyCQjqIHPrTbmjS@database-1.cluster-csh5ndq6v79g.af-south-1.rds.amazonaws.com:5432'
db = SQLAlchemy(app)
#migrate = Migrate(app, db)

@dataclass
class Applications(db.Model):
    student_name = str
    student_email = str

    #id = db.Column(db.Integer, primary_key=True)
    #created = db.Column(db.TIMESTAMP(timezone=False))
    student_name = db.Column(db.Text, primary_key=True)
    student_email = db.Column(db.Text)

@app.route('/applications')
def index():
    applications = Applications.query.all()
    for app in applications:
        print(app.student_name, app.student_email)
    return jsonify(applications)  #render_template('index.html', applications=applications)