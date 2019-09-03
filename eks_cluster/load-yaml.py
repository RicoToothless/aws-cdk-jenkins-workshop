import yaml
import json

with open('kubernetes-resources/hello-k8s.yaml','r') as stream:
    hello_k8s = list(yaml.safe_load_all(stream))

for x in hello_k8s:
    print(x)
