#create a new flask app with route /applications that connects to an external API
from flask import Flask, render_template
import requests
import boto3
from botocore.config import Config

my_config = Config(
    region_name = "af-south-1")

# Create a Secrets Manager client
client = boto3.client('elbv2')

response = client.describe_load_balancers()
for lb in response['LoadBalancers']:
    if lb['DNSName'].startswith("internal-ALB-Applications-API"):
        api_alb = lb['DNSName']

app = Flask(__name__)

@app.route('/applications')
def applications():
    #get the data from the applictions API
    response = requests.get(api_alb)
    print(response)
    applications = response.json()
    print(applications)
    for app in applications:
        print(app)
    return render_template('index.html', data=applications) 

    #return response.json()
