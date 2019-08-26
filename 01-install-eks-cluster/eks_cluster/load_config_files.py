import yaml
import json

def read_k8s_resource(filename):
    with open(filename,'r') as stream:
        return list(yaml.safe_load_all(stream))

def read_docker_daemon_resource(filename):
    with open(filename,'r') as stream:
        return json.dumps(json.load(stream))
