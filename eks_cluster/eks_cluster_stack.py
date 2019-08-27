from aws_cdk import (
    core,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_eks as eks,
)

class EksClusterStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        cluster = eks.Cluster(self, 'hello-eks',
            default_capacity=2,
            default_capacity_instance=ec2.InstanceType('t2.medium')
        )

        cluster.add_resource('hello-kubernetes',
          {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": { "name": "hello-kubernetes" },
            "spec": {
              "type": "LoadBalancer",
              "ports": [ { "port": 80, "targetPort": 8080 } ],
              "selector": { "app": "hello-kubernetes" }
            }
          },
          {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": { "name": "hello-kubernetes" },
            "spec": {
              "replicas": 1,
              "selector": { "matchLabels": { "app": "hello-kubernetes" } },
              "template": {
                "metadata": {
                  "labels": { "app": "hello-kubernetes" }
                },
                "spec": {
                  "containers": [
                    {
                      "name": "hello-kubernetes",
                      "image": "paulbouwer/hello-kubernetes:1.5",
                      "ports": [ { "containerPort": 8080 } ]
                    }
                  ]
                }
              }
            }
           }
        )
