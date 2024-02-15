#!/bin/bash
sudo yum update -y
sudo yum -y install httpd php postgresql15.x86_64 git pip
cd /home/ec2-user/
git clone https://github.com/jojo786/aws-cdk-vpc-ec2-alb-asg.git
cd aws-cdk-vpc-ec2-alb-asg/
git pull
pip install Flask psycopg2-binary requests boto3 gunicorn
cd /home/ec2-user/aws-cdk-vpc-ec2-alb-asg/app/applications/api
gunicorn -w 1 -b 0.0.0.0:5000 'api_flask:app'
#flask --app api_flask run --debug --host=0.0.0.0
cd /home/ec2-user/aws-cdk-vpc-ec2-alb-asg/app/applications/web
gunicorn -w 1 -b 0.0.0.0:5002 'web_flask:app'
#flask --app web_flask run --debug --host=0.0.0.0