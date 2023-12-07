#!/bin/bash
sudo yum update -y
sudo yum -y install httpd php postgresql15.x86_64 git pip
git clone https://github.com/jojo786/aws-cdk-vpc-ec2-alb-asg.git
pip install Flask psycopg2-binary requests
cd /home/ec2-user/aws-cdk-vpc-ec2-alb-asg/app/applications/api
flask --app api_flask run --debug --host=0.0.0.0
cd /home/ec2-user/aws-cdk-vpc-ec2-alb-asg/app/applications/web
flask --app web_flask run --debug --host=0.0.0.0