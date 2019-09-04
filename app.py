#!/usr/bin/env python3

from aws_cdk import core

from eks_cluster.vpc_stack import VpcStack
from eks_cluster.eks_cluster_stack import EksClusterStack


app = core.App()
EksClusterStack(app, "eks-cluster", env=
    {
        'account': '628531345753',
        'region': 'ap-northeast-2'
    }
)

VpcStack(app, "vpc-stack", env=
    {
        'account': '628531345753',
        'region': 'ap-northeast-2'
    }
)

app.synth()
