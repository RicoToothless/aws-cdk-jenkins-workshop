from aws_cdk import (
    core,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_eks as eks,
)

import yaml

with open('kubernetes-resources/hello-k8s.yaml','r') as stream:
    hello_k8s = list(yaml.safe_load_all(stream))

with open('kubernetes-resources/helm-tiller-rbac.yaml','r') as stream:
    helm_tiller_rbac = list(yaml.safe_load_all(stream))

class EksClusterStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        eks_vpc = ec2.Vpc(self, 'eks-vpc',
            cidr='10.66.0.0/16',
            max_azs=2
        )

        cluster = eks.Cluster(self, 'hello-eks',
            vpc=eks_vpc,
            default_capacity=0
        )

        cluster.add_capacity('multi-az-worker-node',
            instance_type=ec2.InstanceType('t3.small'),
            desired_capacity=2,
            key_name='k8s-lab'
        )

        eks_master_role = iam.Role(self, 'AdminRole',
            assumed_by=iam.ArnPrincipal('arn:aws:iam::628531345753:user/Ricoco')
        )

        cluster.aws_auth.add_masters_role(eks_master_role)

        helm_tiller_user = eks.KubernetesResource(self, 'helm-tiller-rbac',
            cluster=cluster,
            manifest=helm_tiller_rbac
        )

        k8s_app = eks.KubernetesResource(self, 'hello-k8s',
            cluster=cluster,
            manifest=hello_k8s
        )
