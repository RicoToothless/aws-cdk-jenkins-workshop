#!/bin/sh

set -x

# delete kubernetes resources

helm delete --purge jenkins-workshop-go-app

helm delete --purge jenkins
kubectl delete pvc jenkins -n jenkins

helm delete --purge istio
helm delete --purge istio-init
helm delete --purge istio-cni
kubectl delete namespace istio-system

# delete ECR repo, EKS cluster & VPC
## CDK ECR (CloudFormation) is not support --force options in delete repository
aws ecr batch-delete-image --repository-name jenkins-workshop-go-app --image-ids imageTag=0.0.1
aws secretsmanager delete-secret --secret-id slack-token-aws --force-delete-without-recovery
## the secrets manager deletion is an asynchronous process. There might be a short delay.
sleep 25
aws secretsmanager describe-secret --secret-id 'slack-token-aws'

export EKS_ADMIN_IAM_USERNAME=`aws sts get-caller-identity | jq '.Arn' | cut -d '"' -s -f2`

cd ../01-install-eks-cluster
cdk destroy -f vpc-stack jenkins-workshop-eks-cluster ecr-repository
cd ../uninstall
