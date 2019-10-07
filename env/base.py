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

bincentive_aws_account = {
    'account': env_or_error('CDK_DEFAULT_ACCOUNT'),
    'region': env_or_default('CDK_DEFAULT_REGION', 'ap-northeast-2')
}

eks_admin_iam_username = env_or_error('EKS_ADMIN_IAM_USERNAME')
