#!/bin/bash
sudo yum update -y
sudo yum -y install httpd php postgresql15.x86_64 git
git clone https://github.com/jojo786/aws-cdk-vpc-ec2-alb-asg.git
sudo chkconfig httpd on
sudo service httpd start