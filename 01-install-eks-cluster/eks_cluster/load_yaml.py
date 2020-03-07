import yaml

def read_k8s_resource(filename):
    with open(filename,'r') as stream:
        return list(yaml.safe_load_all(stream))
