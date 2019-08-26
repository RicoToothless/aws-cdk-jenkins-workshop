#!/bin/sh

ep=$(kubectl get svc istio-ingressgateway -n istio-system -o jsonpath="{.status.loadBalancer.ingress[0].hostname}")

echo "kiali"
echo "http://${ep}:15029"

echo "grafana"
echo "http://${ep}:15031"

echo "prometheus"
echo "http://${ep}:15030"

echo "tracing"
echo "http://${ep}:15032"

echo "jenkins"
echo "http://${ep}"

echo "go-app-example"
echo "http://${ep}/go-app-example"
