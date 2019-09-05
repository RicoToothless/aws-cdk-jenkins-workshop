#!/usr/bin/env python3

from aws_cdk import core

from eks_cluster.vpc_stack import VpcStack
from eks_cluster.eks_cluster_stack import EksClusterStack


app = core.App()

vpc_stack = VpcStack(app, 'vpc-stack', env=
    {
        'account': '628531345753',
        'region': 'ap-northeast-2'
    }
)

eks_cluster_stack = EksClusterStack(app, 'eks-cluster',
    vpc_stack.eks_vpc,
    env=
    {
        'account': '628531345753',
        'region': 'ap-northeast-2'
    }
)

eks_cluster_stack.add_dependency(vpc_stack)

app.synth()
