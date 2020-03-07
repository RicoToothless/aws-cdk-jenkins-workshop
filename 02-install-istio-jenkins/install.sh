#!/bin/sh

# get aws eks kube-config

EKS_CLUSTER_NAME=`aws eks list-clusters | grep jenkinsworkshopekscontrolplane | cut -d '"' -s -f2`
EKS_ADMIN_ARN=`aws iam list-roles | grep jenkins-workshop-eks-cluster-AdminRole | grep Arn | cut -d'"' -s -f4`
EKS_CLUSTER_ARN=`aws eks describe-cluster --name $EKS_CLUSTER_NAME | jq '.cluster.arn' | cut -d '"' -s -f2`

aws eks update-kubeconfig --region ap-northeast-2 --name $EKS_CLUSTER_NAME --role-arn $EKS_ADMIN_ARN

kubectl config use-context $EKS_CLUSTER_ARN

# install istio

helm repo add istio.io https://storage.googleapis.com/istio-release/releases/1.5.0/charts/

helm init --service-account tiller --wait

helm upgrade --install istio-init --namespace istio-system istio.io/istio-init --wait

sleep 10;

helm upgrade --install istio --namespace istio-system -f istio/istio-customized.yaml istio.io/istio --wait

kubectl apply -f istio/addons

kubectl create namespace jenkins

kubectl label namespace jenkins istio-injection=enabled --overwrite=true

# install jenkins

helm upgrade --install --recreate-pods jenkins --namespace jenkins --version 1.9.21 -f jenkins/jenkins-values.yaml stable/jenkins

# kubectl apply -f jenkins/istio-jenkins.yaml
