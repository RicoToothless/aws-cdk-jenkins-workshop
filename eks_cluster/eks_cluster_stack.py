from aws_cdk import (
    core,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_eks as eks,
)

from load_yaml import *

class EksClusterStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, props: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.cluster = eks.Cluster(self, 'eks-control-plane',
            vpc=props,
            default_capacity=0
        )

        self.cluster.add_capacity('worker-node',
            instance_type=ec2.InstanceType('t3.small'),
            desired_capacity=2,
            key_name='k8s-lab'
        )

        eks_master_role = iam.Role(self, 'AdminRole',
            assumed_by=iam.ArnPrincipal('arn:aws:iam::628531345753:user/Ricoco')
        )

        self.cluster.aws_auth.add_masters_role(eks_master_role)

        self.helm_tiller_rbac = eks.KubernetesResource(self, 'helm-tiller-rbac',
           cluster=self.cluster,
            manifest=read_k8s_resource('kubernetes-resources/helm-tiller-rbac.yaml')
        )
