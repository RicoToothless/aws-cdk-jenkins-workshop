from aws_cdk import (
    core,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_eks as eks,
)

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

        cluster.add_resource('hello-k8s',
        )

        cluster.add_resource('helm-tiller',
            {
                "kind": "List",
                "apiVersion": "v1",
                "items": [
                    {
                        "kind": "ServiceAccount",
                        "apiVersion": "v1",
                        "metadata": {
                            "name": "tiller",
                            "namespace": "kube-system"
                        }
                    },
                    {
                        "kind": "ClusterRoleBinding",
                        "apiVersion": "rbac.authorization.k8s.io/v1beta1",
                        "metadata": {
                            "name": "tiller"
                        },
                        "subjects": [
                            {
                                "kind": "ServiceAccount",
                                "name": "tiller",
                                "namespace": "kube-system"
                            }
                        ],
                        "roleRef": {
                            "apiGroup": "rbac.authorization.k8s.io",
                            "kind": "ClusterRole",
                            "name": "cluster-admin"
                        }
                    }
                ]
            }
        )
