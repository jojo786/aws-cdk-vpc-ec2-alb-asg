#!/usr/bin/env python3

from aws_cdk import App, Stack, Tags
from cdk_vpc_ec2.cdk_vpc_stack import CdkVpcStack
#Applications
from cdk_vpc_ec2.cdk_ec2_applications_stack import CdkEc2ApplicationsStack
from cdk_vpc_ec2.cdk_rds_applications_stack import CdkRdsApplicationsStack
#Admin
#from cdk_vpc_ec2.cdk_ec2_admin_stack import CdkEc2AdminStack
#from cdk_vpc_ec2.cdk_rds_admin_stack import CdkRdsAdminStack

app = App()
Tags.of(app).add("Env", "Prod")

vpc_stack = CdkVpcStack(app, "cdk-vpc-infinity")

#Applications Module
ec2_applications_stack = CdkEc2ApplicationsStack(app, "cdk-ec2-infinity-applications",
                        vpc=vpc_stack.vpc)
rds_applications_stack = CdkRdsApplicationsStack(app, "cdk-rds-infinity-applications",
                        vpc=vpc_stack.vpc,
                        asg_security_groups=ec2_applications_stack.asg_api.connections.security_groups)
Tags.of(ec2_applications_stack).add("Module", "Applications")
Tags.of(rds_applications_stack).add("Module", "Applications")

#Admin Module
#ec2_admin_stack = CdkEc2AdminStack(app, "cdk-ec2-infinity-admin",
#                        vpc=vpc_stack.vpc)
#rds_admin_stack = CdkRdsAdminStack(app, "cdk-rds-infinity-admin",
#                        vpc=vpc_stack.vpc,
#                        asg_security_groups=ec2_admin_stack.asg_api.connections.security_groups)
#Tags.of(ec2_admin_stack).add("Module", "Admin")
#Tags.of(rds_admin_stack).add("Module", "Admin")

app.synth()
