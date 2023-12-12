from aws_cdk import CfnOutput, Stack
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_rds as rds
from constructs import Construct

module="Applications"

class CdkRdsApplicationsStack(Stack):

    def __init__(self, scope: Construct, id: str, vpc, asg_security_groups, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        #Create Aurora Cluster with 2 instances with CDK High Level API
        #Secrets Manager auto generate and keep the password, don't put password in cdk code directly
        db_Aurora_cluster = rds.DatabaseCluster(self, f"RDS-AuroraPostgres-{module}",
                                                default_database_name=f"AuroraPostgres{module}",
                                                engine=rds.DatabaseClusterEngine.aurora_postgres(version=rds.AuroraPostgresEngineVersion.VER_13_9),
                                                writer=rds.ClusterInstance.provisioned("writer",
                                                    instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MEDIUM)),
                                                vpc=vpc,
                                                vpc_subnets=ec2.SubnetSelection(subnet_group_name=f"Private-DB-{module}")
                                                )
        
        for asg_sg in asg_security_groups:
            #CfnOutput(self, "RDS SG: ",
            #           value=asg_sg.security_group_id)
            db_Aurora_cluster.connections.allow_default_port_from(asg_sg, "EC2 Autoscaling Group access to Aurora")