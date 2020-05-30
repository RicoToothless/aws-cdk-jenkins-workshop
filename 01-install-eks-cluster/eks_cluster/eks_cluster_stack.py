from aws_cdk import (
    core,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_eks as eks,
)

from eks_cluster.load_config_files import read_k8s_resource, read_docker_daemon_resource
from env import get_eks_admin_iam_username

class EksClusterStack(core.Stack):

    def __init__(self, scope: core.Construct, name: str, vpc: ec2.IVpc, **kwargs) -> None:
        super().__init__(scope, name, **kwargs)

        cluster = eks.Cluster(
            self, 'jenkins-workshop-eks-control-plane',
            vpc=vpc,
            default_capacity=0
        )

        asg_worker_nodes = cluster.add_capacity(
            'worker-node',
            instance_type=ec2.InstanceType('t3.medium'),
            desired_capacity=2,
        )

        asg_jenkins_slave = cluster.add_capacity(
            'worker-node-jenkins-slave',
            instance_type=ec2.InstanceType('t3.medium'),
            desired_capacity=1,
            bootstrap_options=eks.BootstrapOptions(
                kubelet_extra_args='--node-labels jenkins=slave --register-with-taints jenkins=slave:NoSchedule',
                docker_config_json=read_docker_daemon_resource('kubernetes_resources/docker-daemon.json')
            )
        )
        
        asg_worker_nodes.add_to_role_policy(iam.PolicyStatement(
            actions=[
                'secretsmanager:GetSecretValue',
                'secretsmanager:ListSecrets'
                ],
            resources=["*"]
            )
        )

        asg_jenkins_slave.add_to_role_policy(iam.PolicyStatement(
            actions=[
                'ecr:CompleteLayerUpload',
                'ecr:InitiateLayerUpload',
                'ecr:PutImage',
                'ecr:UploadLayerPart'
                ],
            resources=["*"]
            )
        )

        asg_worker_nodes.connections.allow_from(
            asg_jenkins_slave,
            ec2.Port.all_traffic()
        )
        asg_jenkins_slave.connections.allow_from(
            asg_worker_nodes,
            ec2.Port.all_traffic()
        )

        eks_master_role = iam.Role(
            self, 'AdminRole',
            assumed_by=iam.ArnPrincipal(get_eks_admin_iam_username())
        )

        cluster.aws_auth.add_masters_role(eks_master_role)

        helm_tiller_rbac = eks.KubernetesResource(
            self, 'helm-tiller-rbac',
            cluster=cluster,
            manifest=read_k8s_resource('kubernetes_resources/helm-tiller-rbac.yaml')
        )
