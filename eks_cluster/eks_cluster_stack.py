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
            default_capacity=4,
            default_capacity_instance=ec2.InstanceType('t2.medium')
        )

        eks_master_role = iam.Role(self, 'AdminRole',
            assumed_by=iam.ArnPrincipal('your iam user ARN')
        )

        cluster.aws_auth.add_masters_role(eks_master_role)

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

        cluster.add_resource('node-frontend',
            {
               "apiVersion": "v1",
               "kind": "Service",
               "metadata": {
                  "name": "ecsdemo-frontend"
               },
               "spec": {
                  "selector": {
                     "app": "ecsdemo-frontend"
                  },
                  "type": "LoadBalancer",
                  "ports": [
                     {
                        "protocol": "TCP",
                        "port": 80,
                        "targetPort": 3000
                     }
                  ]
               }
            },
            {
               "apiVersion": "apps/v1",
               "kind": "Deployment",
               "metadata": {
                  "name": "ecsdemo-frontend",
                  "labels": {
                     "app": "ecsdemo-frontend"
                  },
                  "namespace": "default"
               },
               "spec": {
                  "replicas": 1,
                  "selector": {
                     "matchLabels": {
                        "app": "ecsdemo-frontend"
                     }
                  },
                  "strategy": {
                     "rollingUpdate": {
                        "maxSurge": "25%",
                        "maxUnavailable": "25%"
                     },
                     "type": "RollingUpdate"
                  },
                  "template": {
                     "metadata": {
                        "labels": {
                           "app": "ecsdemo-frontend"
                        }
                     },
                     "spec": {
                        "containers": [
                           {
                              "image": "brentley/ecsdemo-frontend:latest",
                              "imagePullPolicy": "Always",
                              "name": "ecsdemo-frontend",
                              "ports": [
                                 {
                                    "containerPort": 3000,
                                    "protocol": "TCP"
                                 }
                              ],
                              "env": [
                                 {
                                    "name": "CRYSTAL_URL",
                                    "value": "http://ecsdemo-crystal.default.svc.cluster.local/crystal"
                                 },
                                 {
                                    "name": "NODEJS_URL",
                                    "value": "http://ecsdemo-nodejs.default.svc.cluster.local/"
                                 }
                              ]
                           }
                        ]
                     }
                  }
               }
            }
        )

        cluster.add_resource('node',
            {
               "apiVersion": "v1",
               "kind": "Service",
               "metadata": {
                  "name": "ecsdemo-nodejs"
               },
               "spec": {
                  "selector": {
                     "app": "ecsdemo-nodejs"
                  },
                  "ports": [
                     {
                        "protocol": "TCP",
                        "port": 80,
                        "targetPort": 3000
                     }
                  ]
               }
            },
            {
               "apiVersion": "v1",
               "kind": "Service",
               "metadata": {
                  "name": "ecsdemo-crystal"
               },
               "spec": {
                  "selector": {
                     "app": "ecsdemo-crystal"
                  },
                  "ports": [
                     {
                        "protocol": "TCP",
                        "port": 80,
                        "targetPort": 3000
                     }
                  ]
               }
            },
            {
               "apiVersion": "apps/v1",
               "kind": "Deployment",
               "metadata": {
                  "name": "ecsdemo-nodejs",
                  "labels": {
                     "app": "ecsdemo-nodejs"
                  },
                  "namespace": "default"
               },
               "spec": {
                  "replicas": 3,
                  "selector": {
                     "matchLabels": {
                        "app": "ecsdemo-nodejs"
                     }
                  },
                  "strategy": {
                     "rollingUpdate": {
                        "maxSurge": "25%",
                        "maxUnavailable": "25%"
                     },
                     "type": "RollingUpdate"
                  },
                  "template": {
                     "metadata": {
                        "labels": {
                           "app": "ecsdemo-nodejs"
                        }
                     },
                     "spec": {
                        "containers": [
                           {
                              "image": "brentley/ecsdemo-nodejs:latest",
                              "imagePullPolicy": "Always",
                              "name": "ecsdemo-nodejs",
                              "ports": [
                                 {
                                    "containerPort": 3000,
                                    "protocol": "TCP"
                                 }
                              ]
                           }
                        ]
                     }
                  }
               }
            },
            {
               "apiVersion": "apps/v1",
               "kind": "Deployment",
               "metadata": {
                  "name": "ecsdemo-crystal",
                  "labels": {
                     "app": "ecsdemo-crystal"
                  },
                  "namespace": "default"
               },
               "spec": {
                  "replicas": 3,
                  "selector": {
                     "matchLabels": {
                        "app": "ecsdemo-crystal"
                     }
                  },
                  "strategy": {
                     "rollingUpdate": {
                        "maxSurge": "25%",
                        "maxUnavailable": "25%"
                     },
                     "type": "RollingUpdate"
                  },
                  "template": {
                     "metadata": {
                        "labels": {
                           "app": "ecsdemo-crystal"
                        }
                     },
                     "spec": {
                        "containers": [
                           {
                              "image": "brentley/ecsdemo-crystal:latest",
                              "imagePullPolicy": "Always",
                              "name": "ecsdemo-crystal",
                              "ports": [
                                 {
                                    "containerPort": 3000,
                                    "protocol": "TCP"
                                 }
                              ]
                           }
                        ]
                     }
                  }
               }
            }
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
