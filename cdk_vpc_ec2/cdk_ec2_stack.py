from aws_cdk import CfnOutput, Stack
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as elb
import aws_cdk.aws_autoscaling as autoscaling
from constructs import Construct

ec2_type = "t3.micro"
key_name = "id_rsa"  # Setup key_name for EC2 instance login

with open("./user_data/user_data.sh") as f:
    user_data = f.read()


class CdkEc2ApplicationsStack(Stack):

    def __init__(self, scope: Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create Web ALB
        alb_web = elb.ApplicationLoadBalancer(self, "ALB-Applications-Web",
                                          vpc=vpc,
                                          internet_facing=True,
                                          load_balancer_name="ALB-Applications-Web"
                                          )
        alb_web.connections.allow_from_any_ipv4(
            ec2.Port.tcp(80), "Internet access ALB 80")
        listener = alb_web.add_listener("ALB-Applictions-Web-80",
                                    port=80,
                                    open=True)

        # Create Autoscaling Group with fixed 2*EC2 hosts
        self.asg_web = autoscaling.AutoScalingGroup(self, "ASG-Applications-Web",
                                                vpc=vpc,
                                                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
                                                instance_type=ec2.InstanceType(instance_type_identifier=ec2_type),
                                                machine_image=ec2.MachineImage.latest_amazon_linux2(),
                                                key_name=key_name,
                                                user_data=ec2.UserData.custom(user_data),
                                                desired_capacity=2,
                                                min_capacity=2,
                                                max_capacity=2,
                                                # block_devices=[
                                                #     autoscaling.BlockDevice(
                                                #         device_name="/dev/xvda",
                                                #         volume=autoscaling.BlockDeviceVolume.ebs(
                                                #             volume_type=autoscaling.EbsDeviceVolumeType.GP2,
                                                #             volume_size=12,
                                                #             delete_on_termination=True
                                                #         )),
                                                #     autoscaling.BlockDevice(
                                                #         device_name="/dev/sdb",
                                                #         volume=autoscaling.BlockDeviceVolume.ebs(
                                                #             volume_size=20)
                                                #         # 20GB, with default volume_type gp2
                                                #     )
                                                # ]
                                                )

        self.asg_web.connections.allow_from(alb_web, ec2.Port.tcp(80), "ALB access 80 port of EC2 in Autoscaling Group")
        listener.add_targets("TG-Applications-Web",
                             port=80,
                             targets=[self.asg_web])

        CfnOutput(self, "Output",
                       value=alb_web.load_balancer_dns_name)
        

        # Create API ALB
        alb_api = elb.ApplicationLoadBalancer(self, "ALB-Applications-API",
                                          vpc=vpc,
                                          internet_facing=True,
                                          load_balancer_name="ALB-Applications-API"
                                          )
        #Need to modify to allow access from Web SG
        alb_web.connections.allow_from_any_ipv4(
            ec2.Port.tcp(80), "Internet access ALB 80")
        
        listener = alb_api.add_listener("ALB-Applictions-API-80",
                                    port=80,
                                    open=True)

        # Create Autoscaling Group with fixed 2*EC2 hosts
        self.asg_api = autoscaling.AutoScalingGroup(self, "ASG-Applications-API",
                                                vpc=vpc,
                                                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
                                                instance_type=ec2.InstanceType(instance_type_identifier=ec2_type),
                                                machine_image=ec2.MachineImage.latest_amazon_linux2(),
                                                key_name=key_name,
                                                user_data=ec2.UserData.custom(user_data),
                                                desired_capacity=2,
                                                min_capacity=2,
                                                max_capacity=2,
                                                )

        self.asg_api.connections.allow_from(alb_api, ec2.Port.tcp(80), "ALB API access 80 port of EC2 in Autoscaling Group")
        listener.add_targets("TG-Applications-API",
                             port=80,
                             targets=[self.asg_api])
