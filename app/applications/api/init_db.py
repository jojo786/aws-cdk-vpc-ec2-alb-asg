import psycopg2
import boto3
from botocore.exceptions import ClientError
import json
from faker import Faker


def get_secret():

    secret_name = "RDSAuroraPostgresApplicatio-ZdX5r4dOewvx"
    region_name = "af-south-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

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

user, password, host, port = get_secret()

conn = psycopg2.connect(
    user=user, 
    password=password, 
    host=host,
    port=port) 
  
# create a cursor 
cur = conn.cursor() 

#insert_statements = []
fake = Faker()

for i in range(10):
    fake_data = {
        "name": fake.name(),
        "email": fake.email(),
    }
    name = fake_data['name']
    email = fake_data['email']
    statement = """INSERT INTO applications (student_name, student_email) VALUES(%s, %s);""" 
    print(statement)
    cur.execute(statement, (name, email)) 
    conn.commit()
  
# close the cursor and connection 
cur.close() 
conn.close() 


