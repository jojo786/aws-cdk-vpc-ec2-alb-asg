import aws_cdk as cdk
from aws_cdk import CfnOutput, Stack
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as elb
from aws_cdk import aws_autoscaling as autoscaling
import aws_cdk.aws_certificatemanager as acm
from constructs import Construct
from pathlib import Path
import aws_cdk.aws_iam as iam
import aws_cdk.aws_wafv2 as wafv2 


module='Applications'
ec2_type = 't3.micro'
key_name = 'id_rsa'  # Setup key_name for EC2 instance login
web_ami='ami-0d26d710133765696'
api_ami='ami-0d26d710133765696'

data_folder = Path("user_data/")
file_to_open = data_folder / "user_data.sh"
#print(file_to_open.read_text())
with open(file_to_open) as f:
   user_data = f.read()

class CdkEc2ApplicationsStack(Stack):

    def __init__(self, scope: Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create Web ALB
        alb_web = elb.ApplicationLoadBalancer(self, f"ALB-{module}-Web",
                                          vpc=vpc,
                                          vpc_subnets=ec2.SubnetSelection(subnet_group_name=f'Public-{module}-Web-ALB'),
                                          internet_facing=True,
                                          load_balancer_name=f"ALB-{module}-Web"
                                          )

        # Create Web ALB Listener - Port 80, redirect to port 5002
        alb_web_listener = alb_web.add_listener(f"ALB-{module}-Web-80",
                                    port=80,
                                    open=True,
                                    protocol=elb.ApplicationProtocol.HTTP,
                                    default_action=elb.ListenerAction.redirect(host="#{host}", 
                                                         path="/#{path}", 
                                                         permanent=True, 
                                                         port="5002", 
                                                         protocol="HTTP", 
                                                         query="#{query}")
        )
        


         #Allow Web ALB connections on port 80 from the internet
        alb_web.connections.allow_from_any_ipv4(
            ec2.Port.tcp(80), "Internet access ALB 80")
        
    

        """ #Create ACM HTTPS cert
        cert = acm.Certificate(self, "Certificate",
            domain_name="hello.example.com",
            validation=acm.CertificateValidation.from_dns()

        # Create Web ALB Listener
        alb_web_listener = alb_web.add_listener(f"ALB-{module}-Web-443",
                                    port=443,
                                    open=True,
                                    certificate_name='Certificate')
        
        # Allow Web ALB connections on port 443 from the internet
        alb_web.connections.allow_from_any_ipv4(
            ec2.Port.tcp(443), "Internet access ALB 443") """

        #IAM Instance Role to attached to EC2 instances in ASG
        role = iam.Role(self, "Role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")  
        )

        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("SecretsManagerReadWrite"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("ElasticLoadBalancingReadOnly"))

        # Create Web Autoscaling Group 
        self.asg_web = autoscaling.AutoScalingGroup(self, f"ASG-{module}-Web",
                                                vpc=vpc,
                                                vpc_subnets=ec2.SubnetSelection(subnet_group_name=f'Private-{module}-Web-ASG'),
                                                instance_type=ec2.InstanceType(instance_type_identifier=ec2_type),
                                                #machine_image=ec2.MachineImage.latest_amazon_linux2(),
                                                machine_image=ec2.MachineImage.generic_linux({
                                                     "af-south-1": web_ami
                                                }),
                                                key_name=key_name,
                                                user_data=ec2.UserData.custom(user_data),
                                                #desired_capacity=2,
                                                min_capacity=1,
                                                max_capacity=3,
                                                role=role,
                                                )
        self.asg_web.scale_on_cpu_utilization(
            f"CPUScaling-{module}-Web",
            target_utilization_percent=25,
            cooldown=cdk.Duration.seconds(60),
            disable_scale_in=False,
            estimated_instance_warmup=cdk.Duration.seconds(60)
        )

        #self.asg_web.connections.allow_from(alb_web, ec2.Port.tcp(80), "ALB access 80 port of EC2 in Autoscaling Group")
        self.asg_web.connections.allow_from(alb_web, ec2.Port.tcp(5002), "ALB access 5002 port of EC2 in Autoscaling Group")

        #alb_web_listener.add_targets(f"TG-{module}-Web-80",
        #                     port=80,
        #                     targets=[self.asg_web])
        
        alb_web_listener.add_targets(f"TG-{module}-Web-5002",
                             port=5002,
                             protocol=elb.ApplicationProtocol.HTTP,
                             targets=[self.asg_web])

        CfnOutput(self, "Output",
                       value=alb_web.load_balancer_dns_name)
        

        ############## Create API Internal ALB
        alb_api = elb.ApplicationLoadBalancer(self, f"ALB-{module}-API",
                                          vpc=vpc,  vpc_subnets=ec2.SubnetSelection(subnet_group_name=f'Private-{module}-API-ALB'),
                                          internet_facing=False,
                                          load_balancer_name=f"ALB-{module}-API"
                                          )
        

        #Allow port 80 on ALB
        #alb_api.connections.allow_from_any_ipv4(
        #    ec2.Port.tcp(80), "Internet access ALB 80")

        alb_api.connections.allow_from(self.asg_web, ec2.Port.tcp(80), "Allow Web ASG to connect to ALB API on port 80")

        
        # Create Internal API ALB Listener on port 80, redirect to port 5000
        alb_api_listener = alb_api.add_listener(f"ALB-{module}-API-80",
                                    port=80,
                                    open=True,
                                    protocol=elb.ApplicationProtocol.HTTP,
                                    default_action=elb.ListenerAction.redirect(host="#{host}", 
                                                         path="/#{path}", 
                                                         permanent=True, 
                                                         port="5000", 
                                                         protocol="HTTP", 
                                                         query="#{query}")
                                    )    


        # Create Autoscaling Group
        self.asg_api = autoscaling.AutoScalingGroup(self, f"ASG-{module}-API",
                                                vpc=vpc,
                                                vpc_subnets=ec2.SubnetSelection(subnet_group_name=f'Private-{module}-API-ASG'),
                                                instance_type=ec2.InstanceType(instance_type_identifier=ec2_type),
                                                machine_image=ec2.MachineImage.generic_linux({
                                                    "af-south-1": api_ami
                                                }),
                                                key_name=key_name,
                                                user_data=ec2.UserData.custom(user_data),
                                                #desired_capacity=2,
                                                min_capacity=1,
                                                max_capacity=3,
                                                role=role,
                                                )

        self.asg_api.scale_on_cpu_utilization(
                            f"CPUScaling-{module}-Web",
                            target_utilization_percent=25,
                            cooldown=cdk.Duration.seconds(60),
                            disable_scale_in=False,
                            estimated_instance_warmup=cdk.Duration.seconds(60)
                        )

        self.asg_api.connections.allow_from(alb_api, ec2.Port.tcp(5000), "ALB API access to port 5000 of EC2 in Autoscaling Group")

        alb_api_listener.add_targets(f"TG-{module}-API",
                             port=5000,
                             protocol=elb.ApplicationProtocol.HTTP,
                             targets=[self.asg_api])

        #cfn_instance_connect_endpoint = ec2.CfnInstanceConnectEndpoint(self, "MyCfnInstanceConnectEndpoint",
        #    subnet_id = vpc.select_subnets(subnet_group_name='Private-{module}-Web-ASG').subnet_ids[0]
        #)