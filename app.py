#!/usr/bin/env python3

import imp

from aws_cdk import core

from eks_cluster.vpc_stack import VpcStack
from eks_cluster.eks_cluster_stack import EksClusterStack

os_env = imp.load_source('base', 'env/base.py')

app = core.App()

vpc_stack = VpcStack(app, 'vpc-stack', env=os_env.bincentive_aws_account)

eks_cluster_stack = EksClusterStack(app, 'eks-cluster',
        vpc_stack.eks_vpc, env=os_env.bincentive_aws_account)

eks_cluster_stack.add_dependency(vpc_stack)

app.synth()
