#!/usr/bin/env python3

from aws_cdk import core

from eks_cluster.eks_cluster_stack import EksClusterStack


app = core.App()
EksClusterStack(app, "eks-cluster")

app.synth()
