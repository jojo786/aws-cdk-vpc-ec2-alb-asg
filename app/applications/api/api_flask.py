import os
from flask import Flask, jsonify
import psycopg2
import boto3
from botocore.exceptions import ClientError
from botocore.config import Config
import json


def get_secret():

    secret_name = "RDSAuroraPostgresApplicatio-V0yAz1ZwObfA"
    my_config = Config(
        region_name = "af-south-1")

    # Create a Secrets Manager client
    client = boto3.client('secretsmanager', config=my_config)

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    
    secretstring = get_secret_value_response['SecretString']
    secret = json.loads(secretstring)
    user = secret['username']
    host = secret['host']
    password = secret['password']
    port = secret['port']
    return user, password, host, port

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
user, password, host, port = get_secret()
print (host)

@app.route('/applications')
def index():
    conn = psycopg2.connect(
                            user=user, 
                            password=password, 
                            host=host,
                            port=port) 
  
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