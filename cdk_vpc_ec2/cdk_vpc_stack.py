from aws_cdk import CfnOutput, Stack
import aws_cdk.aws_ec2 as ec2
from constructs import Construct

class CdkVpcStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # configuration will create 3 groups in 2 AZs = 6 subnets.
        self.vpc = ec2.Vpc(self, "VPC-Infinity",
                           max_azs=2,
                           ip_addresses=ec2.IpAddresses.cidr("10.10.0.0/16"),
                           subnet_configuration=[ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PUBLIC,
                               name="Public-Applications",
                               cidr_mask=24
                           ), ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                               name="Private-Applications",
                               cidr_mask=24
                           ), ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                               name="DB-Applications",
                               cidr_mask=24
                           )
                           ],
                           # nat_gateway_provider=ec2.NatProvider.gateway(),
                           nat_gateways=2,
                           )
        CfnOutput(self, "Output",
                       value=self.vpc.vpc_id)
