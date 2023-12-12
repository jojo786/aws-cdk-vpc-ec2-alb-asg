from aws_cdk import CfnOutput, Stack
import aws_cdk.aws_ec2 as ec2
from constructs import Construct
from pathlib import Path

class CdkVpcStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        module1="Applications"
        module2="Admin"
        
        self.vpc = ec2.Vpc(self, "VPC-Infinity",
                           max_azs=2,
                           nat_gateways=4,
                           ip_addresses=ec2.IpAddresses.cidr("10.10.0.0/16"),
                           subnet_configuration=[
                               #Applications Module: configuration will create 5 groups in 2 AZs = 10 subnets
                               ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PUBLIC,
                               name=f"Public-{module1}-Web-ALB",
                               cidr_mask=24
                           ), ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                               name=f"Private-{module1}-Web-ASG",
                               cidr_mask=24
                           ), ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                               name=f"Private-{module1}-API-ALB",
                               cidr_mask=24    
                           ), ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                               name=f"Private-{module1}-API-ASG",
                               cidr_mask=24 
                           ), ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                               name=f"Private-DB-{module1}",
                               cidr_mask=24
                               #Admin Module: configuration will create 5 groups in 2 AZs = 10 subnets.
                        #    ), ec2.SubnetConfiguration(
                        #        subnet_type=ec2.SubnetType.PUBLIC,
                        #        name=f"Public-{module2}-Web-ALB",
                        #        cidr_mask=24
                        #    ), ec2.SubnetConfiguration(
                        #        subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                        #        name=f"Private-{module2}-Web-ASG",
                        #        cidr_mask=24
                        #    ), ec2.SubnetConfiguration(
                        #        subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                        #        name=f"Private-{module2}-API-ALB",
                        #        cidr_mask=24    
                        #    ), ec2.SubnetConfiguration(
                        #        subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                        #        name=f"Private-{module2}-API-ASG",
                        #        cidr_mask=24 
                        #    ), ec2.SubnetConfiguration(
                        #        subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                        #        name=f"Private-DB-{module2}",
                        #        cidr_mask=24
                             )
                           ]
                           )
        CfnOutput(self, "Output",
                       value=self.vpc.vpc_id)
