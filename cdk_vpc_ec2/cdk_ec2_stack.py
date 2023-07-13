from aws_cdk import CfnOutput, Stack
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as elb
import aws_cdk.aws_autoscaling as autoscaling
import aws_cdk.aws_certificatemanager as acm
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
                                          vpc_subnets=ec2.SubnetSelection(subnet_group_name='Public-Applications-Web-ALB'),
                                          internet_facing=True,
                                          load_balancer_name="ALB-Applications-Web"
                                          )
        
        
        # Create Web ALB Listener
        alb_web_listener = alb_web.add_listener("ALB-Applications-Web-80",
                                    port=80,
                                    open=True)
        
        # Allow Web ALB connections on port 80 from the internet
        alb_web.connections.allow_from_any_ipv4(
            ec2.Port.tcp(80), "Internet access ALB 80")
        

        """ #Create ACM HTTPS cert
        cert = acm.Certificate(self, "Certificate",
            domain_name="hello.example.com",
            validation=acm.CertificateValidation.from_dns()

        # Create Web ALB Listener
        alb_web_listener = alb_web.add_listener("ALB-Applications-Web-443",
                                    port=443,
                                    open=True,
                                    certificate_name='Certificate')
        
        # Allow Web ALB connections on port 80 from the internet
        alb_web.connections.allow_from_any_ipv4(
            ec2.Port.tcp(443), "Internet access ALB 443") """

        # Create Web Autoscaling Group with fixed 2*EC2 hosts
        self.asg_web = autoscaling.AutoScalingGroup(self, "ASG-Applications-Web",
                                                vpc=vpc,
                                                vpc_subnets=ec2.SubnetSelection(subnet_group_name='Private-Applications-Web-ASG'),
                                                instance_type=ec2.InstanceType(instance_type_identifier=ec2_type),
                                                #machine_image=ec2.MachineImage.latest_amazon_linux2(),
                                                machine_image=ec2.MachineImage.generic_linux({
                                                    "af-south-1": "ami-00ecb2c6959112464",
                                                    "eu-west-1": "ami-12345678"
                                                }),
                                                key_name=key_name,
                                                user_data=ec2.UserData.custom(user_data),
                                                desired_capacity=2,
                                                min_capacity=2,
                                                max_capacity=2,
                                                )

        self.asg_web.connections.allow_from(alb_web, ec2.Port.tcp(80), "ALB access 80 port of EC2 in Autoscaling Group")

        alb_web_listener.add_targets("TG-Applications-Web",
                             port=80,
                             targets=[self.asg_web])

        CfnOutput(self, "Output",
                       value=alb_web.load_balancer_dns_name)
        

        # Create API Internal ALB
        alb_api = elb.ApplicationLoadBalancer(self, "ALB-Applications-API",
                                          vpc=vpc,  vpc_subnets=ec2.SubnetSelection(subnet_group_name='Private-Applications-API-ALB'),
                                          internet_facing=False,
                                          load_balancer_name="ALB-Applications-API"
                                          )
        
        #Allow port 80
        alb_api.connections.allow_from_any_ipv4(
            ec2.Port.tcp(80), "Internet access ALB 80")
        
        # Create API ALB Listener
        alb_api_listener = alb_api.add_listener("ALB-Applications-API-80",
                                    port=80,
                                    open=True)

        # Create Autoscaling Group with fixed 2*EC2 hosts
        self.asg_api = autoscaling.AutoScalingGroup(self, "ASG-Applications-API",
                                                vpc=vpc,
                                                vpc_subnets=ec2.SubnetSelection(subnet_group_name='Private-Applications-API-ASG'),
                                                instance_type=ec2.InstanceType(instance_type_identifier=ec2_type),
                                                machine_image=ec2.MachineImage.generic_linux({
                                                    "af-south-1": "ami-00ecb2c6959112464",
                                                    "eu-west-1": "ami-12345678"
                                                }),
                                                key_name=key_name,
                                                user_data=ec2.UserData.custom(user_data),
                                                desired_capacity=2,
                                                min_capacity=2,
                                                max_capacity=2,
                                                )

        self.asg_api.connections.allow_from(alb_api, ec2.Port.tcp(80), "ALB API access 80 port of EC2 in Autoscaling Group")
        
        alb_api_listener.add_targets("TG-Applications-API",
                             port=80,
                             targets=[self.asg_api])
