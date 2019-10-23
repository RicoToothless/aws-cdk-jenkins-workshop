#!/usr/bin/env python3

from aws_cdk import core

from eks_cluster.vpc_stack import VpcStack
from eks_cluster.eks_cluster_stack import EksClusterStack
from env import bincentive_aws_account

app = core.App()

vpc_stack = VpcStack(app, 'vpc-stack', env=bincentive_aws_account)

eks_cluster_stack = EksClusterStack(app, 'eks-cluster', vpc=vpc_stack.eks_vpc, env=bincentive_aws_account)

eks_cluster_stack.add_dependency(vpc_stack)

app.synth()
