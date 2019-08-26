from aws_cdk import (
    core,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_eks as eks,
)

class EksClusterStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        cluster = eks.Cluster(self, 'hello-eks',
            default_capacity=2,
            default_capacity_instance=ec2.InstanceType('t2.medium')
        )
