#!/usr/bin/env python3

from aws_cdk import App

from cdk_vpc_ec2.cdk_vpc_stack import CdkVpcStack
from cdk_vpc_ec2.cdk_ec2_stack import CdkEc2ApplicationsStack
from cdk_vpc_ec2.cdk_rds_stack import CdkRdsApplicationsStack

app = App()

vpc_stack = CdkVpcStack(app, "cdk-vpc-infinity")
ec2_applictions_stack = CdkEc2ApplicationsStack(app, "cdk-ec2-infinity-applications",
                        vpc=vpc_stack.vpc)
rds_applictions_stack = CdkRdsApplicationsStack(app, "cdk-rds-infinity-applications",
                        vpc=vpc_stack.vpc,
                        asg_security_groups=ec2_applictions_stack.asg_web.connections.security_groups)

app.synth()
