#create a new flask app with route /applications that connects to an external API
from flask import Flask, request, render_template, redirect, url_for
import requests


app = Flask(__name__)
@app.route('/applications')
def applications():
    #get the data from the applictions API
    response = requests.get('internal-ALB-Applications-API-721549299.af-south-1.elb.amazonaws.com:5000/applications')
    applications = response.json()
    print(applications)
    for app in applications:
        print(app)
    return render_template('index.html', data=applications) 

    #return response.json()
