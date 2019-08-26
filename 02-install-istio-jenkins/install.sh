#!/bin/sh

set -e
set -x

# install helm & kubectl cli

wget https://get.helm.sh/helm-v2.16.1-linux-amd64.tar.gz
tar -zxvf helm-v2.16.1-linux-amd64.tar.gz
sudo mv linux-amd64/helm /usr/local/bin/helm
rm -r helm-v2.16.1-linux-amd64.tar.gz  linux-amd64/

sudo apt-get update && sudo apt-get install -y apt-transport-https
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
sudo apt-get install -y kubectl

# get aws eks kube-config

EKS_CLUSTER_NAME=`aws eks list-clusters | grep jenkinsworkshopekscontrolplane | cut -d '"' -s -f2`
EKS_ADMIN_ARN=`aws iam list-roles | grep jenkins-workshop-eks-cluster-AdminRole | grep Arn | cut -d'"' -s -f4`
EKS_CLUSTER_ARN=`aws eks describe-cluster --name $EKS_CLUSTER_NAME | jq '.cluster.arn' | cut -d '"' -s -f2`

aws eks update-kubeconfig --region ap-northeast-2 --name $EKS_CLUSTER_NAME --role-arn $EKS_ADMIN_ARN

kubectl config use-context $EKS_CLUSTER_ARN

# install istio

helm init --service-account tiller --wait

helm repo add istio.io https://storage.googleapis.com/istio-release/releases/1.5.0/charts/

helm upgrade --install istio-init --namespace istio-system istio.io/istio-init --wait

sleep 10;

helm upgrade --install istio --namespace istio-system -f istio/istio-customized.yaml istio.io/istio --wait

kubectl apply -f istio/addons

kubectl apply -f istio/http-gateway.yaml

kubectl create namespace jenkins

# install jenkins

helm upgrade --install --recreate-pods jenkins --namespace jenkins --version 1.9.21 -f jenkins/jenkins-values.yaml stable/jenkins

kubectl apply -f jenkins/istio-jenkins.yaml

kubectl create clusterrole jenkins --verb=get,list,create --resource=pods,pods/portforward

kubectl create clusterrolebinding jenkins-binding --clusterrole=jenkins --serviceaccount=jenkins:jenkins
