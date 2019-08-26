import os
import sys


def env_or_default(name, default):
    return os.environ.get(name, default)

def env_or_error(name):
    env = os.environ.get(name)
    if env is None:
        print(f'ERROR: Environment variable {name} is required, but was not set.')
        sys.exit(1)
    return env

def get_eks_admin_iam_username():
    return env_or_error('EKS_ADMIN_IAM_USERNAME')

cdk_default_account = os.environ.get('CDK_DEFAULT_ACCOUNT')
cdk_default_region = os.environ.get('CDK_DEFAULT_REGION')

aws_account = {
    'account': env_or_default('CDK_ACCOUNT', cdk_default_account),
    'region': env_or_default('CDK_REGION', cdk_default_region)
}
