import os
from flask import Flask, jsonify
import psycopg2

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)


@app.route('/applications')
def index():
    conn = psycopg2.connect(
                            user="postgres", 
                            password="eqiQSWyCQjqIHPrTbmjS", 
                            host="database-1.cluster-csh5ndq6v79g.af-south-1.rds.amazonaws.com", 
                            port="5432") 
  
    # create a cursor 
    cur = conn.cursor() 
  
    # Select all products from the table 
    cur.execute('''SELECT * FROM applications''') 
  
    # Fetch the data 
    applications = cur.fetchall() 
  
    # close the cursor and connection 
    cur.close() 
    conn.close() 
    for app in applications:
        print(app)
    return jsonify(applications)