#create new flask application with db connection to postgres
import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
#from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:eqiQSWyCQjqIHPrTbmjS@database-1.cluster-csh5ndq6v79g.af-south-1.rds.amazonaws.com:5432'
db = SQLAlchemy(app)
#migrate = Migrate(app, db)

class Applications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime(timezone=True))
    student_id = db.Column(db.String(100), nullable=False)
    app_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Applications {self.student_id}>'


@app.route('/applications')
def index():
    applications = Applications.query.all()
    return applications  #render_template('index.html', applications=applications)