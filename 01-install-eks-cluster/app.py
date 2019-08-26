#!/usr/bin/env python3

from aws_cdk import core

from eks_cluster.vpc_stack import VpcStack
from eks_cluster.eks_cluster_stack import EksClusterStack
from ecr.ecr_stack import EcrStack
from env import aws_account

app = core.App()

# VPC

vpc_stack = VpcStack(app, 'vpc-stack', env=aws_account)

# EKS

eks_cluster_stack = EksClusterStack(app, 'jenkins-workshop-eks-cluster', vpc=vpc_stack.eks_vpc, env=aws_account)

eks_cluster_stack.add_dependency(vpc_stack)

# ECR

ecr_repository_stack = EcrStack(app, 'ecr-repository', env=aws_account)

app.synth()
