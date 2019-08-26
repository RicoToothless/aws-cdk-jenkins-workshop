from aws_cdk import (
    core,
    aws_ec2 as ec2,
)

class VpcStack(core.Stack):

    def __init__(self, scope: core.Construct, name: str, **kwargs) -> None:
        super().__init__(scope, name, **kwargs)

        public_subnet = ec2.SubnetConfiguration(
            cidr_mask=20,
            name='Ingress',
            subnet_type=ec2.SubnetType.PUBLIC
        )

        private_subnet = ec2.SubnetConfiguration(
            cidr_mask=20,
            name='Application',
            subnet_type=ec2.SubnetType.PRIVATE
        )

        self.eks_vpc = ec2.Vpc(
            self, 'eks-vpc',
            cidr='10.1.0.0/16',
            max_azs=2,
            subnet_configuration=[public_subnet, private_subnet]
        )
