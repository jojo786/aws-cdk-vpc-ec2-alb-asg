import aws_cdk as cdk
from aws_cdk import CfnOutput, Stack
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as elb
from aws_cdk import aws_autoscaling as autoscaling
import aws_cdk.aws_certificatemanager as acm
from constructs import Construct
from pathlib import Path
import aws_cdk.aws_iam as iam


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

        # Create Web ALB Listener - HTTP Port 80
        alb_web_listener_80 = alb_web.add_listener(f"ALB-{module}-Web-80",
                                    port=80,
                                    open=True,
                                    protocol=elb.ApplicationProtocol.HTTP,
        )
        


         #Allow Web ALB connections on port 80 from the internet
        alb_web.connections.allow_from_any_ipv4(
            ec2.Port.tcp(80), "ALLOW FROM Internet/All TO ALB-WEB port 80")

        # create ACM SSL cert
        new_cert = acm.Certificate(self, "New Certificate",
            domain_name="hello.hacksaw.co.za",
            validation=acm.CertificateValidation.from_dns() 
            )

         # existing HTTPS cert
        existing_cert = acm.Certificate.from_certificate_arn(self, "Existing Certificate",
            certificate_arn='arn:aws:acm:af-south-1:718974227478:certificate/5a55a6e1-b1be-4113-bc7b-87c2f00132d6'
            )

        # Create Web ALB Listener - HTTPS Port 443, with cert
        alb_web_listener_443 = alb_web.add_listener(f"ALB-{module}-Web-443",
                                    port=443,
                                    open=True,
                                    certificates=[existing_cert],
                                    protocol=elb.ApplicationProtocol.HTTPS,
                                    #default_action=elb.ListenerAction.redirect(host="#{host}", 
                                    #                     path="/#{path}", 
                                    #                     permanent=True, 
                                    #                     port="80", 
                                    #                     protocol="HTTP", 
                                    #                     query="#{query}") 
                                    )
        
        # Allow Web ALB connections on port 443 from the internet
        alb_web.connections.allow_from_any_ipv4(
            ec2.Port.tcp(443), "Allow FROM All/Internet TO ALB-WEB on port 443")

        #IAM Instance Role to attached to EC2 instances in ASG
        role = iam.Role(self, "Role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")  
        )

        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("SecretsManagerReadWrite"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("ElasticLoadBalancingReadOnly"))

        # Create Web AutoScaling Group (ASG)
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

        #Allow port 80 on EC2 in ASG from ALB (dont need port 443 to be allowed on ASG)
        self.asg_web.connections.allow_from(alb_web, ec2.Port.tcp(80), "Allow FROM ALB-WEB TO port 80 on ASG-WE")

        #Add the ASG to ALB port 80 listener on port 5002, so redirect from ALB 80 to 5002 on the ASG
        alb_web_listener_80.add_targets(f"TG-{module}-Web-80",
                             port=5002,
                             protocol=elb.ApplicationProtocol.HTTP,
                             targets=[self.asg_web])
        
        #Add the ASG to ALB port 443 listener on port 80 - so HTTPS on ALB will be sent to HTTP on ASG
        alb_web_listener_443.add_targets(f"TG-{module}-Web-80",
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

        alb_api.connections.allow_from(self.asg_web, ec2.Port.tcp(80), "Allow FROM ASG-WEB TO ALB-API on port 80")

        
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

        self.asg_api.connections.allow_from(alb_api, ec2.Port.tcp(5000), "Allow FROM ALB-API to port 5000 on ASG-API")
        
        
        alb_api_listener.add_targets(f"TG-{module}-API",
                             port=5000,
                             protocol=elb.ApplicationProtocol.HTTP,
                             targets=[self.asg_api])

        #cfn_instance_connect_endpoint = ec2.CfnInstanceConnectEndpoint(self, "MyCfnInstanceConnectEndpoint",
        #    subnet_id = vpc.select_subnets(subnet_group_name='Private-{module}-Web-ASG').subnet_ids[0]
        #)