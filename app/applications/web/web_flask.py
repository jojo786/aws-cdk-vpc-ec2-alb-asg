#create a new flask app with route /applications that connects to an external API
from flask import Flask, request, render_template, redirect, url_for
import requests


app = Flask(__name__)
@app.route('/applications')
def applications():
    #get the data from the applictions API
    response = requests.get('http://127.0.0.1:5000/applications')
    print(response)
    return render_template('index.html', data=response) 

    #return response.json()
