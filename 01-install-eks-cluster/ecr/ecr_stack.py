from aws_cdk import (
    core,
    aws_ecr as ecr,
)

class EcrStack(core.Stack):

    def __init__(self, scope: core.Construct, name: str, **kwargs) -> None:
        super().__init__(scope, name, **kwargs)

        app_repositories = [
            'jenkins-workshop-go-app'
        ]

        default_ecr_lifecyclerule = ecr.LifecycleRule(
            description='Default ECR lifecycle Rule',
            max_image_count=500,
            rule_priority=100
        )

        for a in app_repositories:
            ecr.Repository(
                self, a,
                repository_name=a,
                lifecycle_rules=[default_ecr_lifecyclerule],
                removal_policy=core.RemovalPolicy.DESTROY
            )
