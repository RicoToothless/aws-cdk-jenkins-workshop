#!/bin/sh

set -e
set -x

sudo apt install jq -y
export EKS_ADMIN_IAM_USERNAME=`aws sts get-caller-identity | jq '.Arn' | cut -d '"' -s -f2`
echo $EKS_ADMIN_IAM_USERNAME
pip3 install --no-cache-dir -r requirements.txt
cdk bootstrap
cdk list
cdk deploy --require-approval never vpc-stack jenkins-workshop-eks-cluster ecr-repository
