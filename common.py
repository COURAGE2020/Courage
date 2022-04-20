import logging
import os
import time
import constants
import aws_support.string_utils as su
from aws_support import AwsClient

logger = logging.getLogger(constants.LOGGER_NAME)
AWS_CLIENT: AwsClient


# Functions
def get_aws_account_id(env):
    logger.debug(f"get_aws_account_id({env})")

    return constants.ENV_TO_ACCOUNT_MAP[env]['account_id']


def get_aws_account_env(env):
    logger.debug(f"get_aws_account_env({env})")

    return constants.ENV_TO_ACCOUNT_MAP[env]['account_env']


def create_assumed_role_arn(env, region):
    logger.debug(f"create_assumed_role_arn({env}, {region})")

    account_id = get_aws_account_id(env)
    account_env = get_aws_account_env(env)

    role_arn = su.replace_account(constants.JENKINS_ASSUMED_ROLE_ARN,
                                  account_id)
    role_arn = su.replace_account_env(role_arn, account_env)
    role_arn = su.replace_region(role_arn, region)
    return role_arn


def setup_aws_client(args):
    logger.debug(f"setup_aws_client({args})")
    global AWS_CLIENT
    AWS_CLIENT = AwsClient(args.get('env'), args.get('region'), constants.LOGGER_NAME,
                           args.get('profile'), constants.MAX_ATTEMPTS)
    role_arn = create_assumed_role_arn(args.get('env'), args.get('region'))
    AWS_CLIENT.assume_role(role_arn, constants.JENKINS_SESSION_ID)


# def create_lambda_bucket_name(args):
#     logger.debug(f"create_lambda_bucket_name({args})")

#     bucket_name = su.replace_region(constants.S3_LAMBDA_REPO, args['region'])
#     return bucket_name


# def create_lambda_key(args):
#     logger.debug(f"create_lambda_key({args})")

#     key = f"{args['project']}/{args['app']}/{args['version']}" \
#         f"/{args['app']}.zip"
#     return key


def run_info(args):
    missing_value = 'Unknown'
    info = {
        'Project': args.get('project', missing_value),
        'App': args.get('app', missing_value),
        'Env': args.get('env', missing_value),
        'Submitter': os.getenv('CODEBUILD_INITIATOR', missing_value),
        'JobName': os.getenv('CODEBUILD_BUILD_ID', missing_value).split(':')[0],
        'Version': args.get('version', missing_value),
        'Region': args.get('region', missing_value),
        'Duration': int(os.getenv('CODEBUILD_START_TIME', int(time.time() * 1000))),
        'Status': 'Fail',
        'BuildNumber': os.getenv('CODEBUILD_BUILD_NUMBER', missing_value)
    }
    return info
