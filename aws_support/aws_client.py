import logging
import boto3
from botocore.config import Config


class AwsClient(object):
    def __init__(self, env, region, logger_name, profile=None, max_attempts=3):
        self.env = env
        self.region = region
        self.profile = profile
        self.assumed_role_keys = {}
        self.config = Config(retries=dict(max_attempts=max_attempts))
        self.logger = logging.getLogger(logger_name)

        if self.profile:
            boto3.setup_default_session(profile_name=self.profile,
                                        region_name=self.region)

    def client(self, service_name):
        self.logger.debug(f"client({service_name})")

        client = boto3.client(service_name,
                              region_name=self.region,
                              config=self.config)
        return client

    def assume_role(self, role_arn, session_id):
        self.logger.debug(f"assume_role({role_arn}, {session_id})")

        client = self.client('sts')
        response = client.assume_role(
            RoleArn=role_arn,
            RoleSessionName=session_id
        )
        self.logger.debug(f" response => {response}")
        self.assumed_role_keys = response['Credentials']

    def assumed_role_client(self, service_name):
        self.logger.debug(f"get_assumed_role_client(self, {service_name})")

        client = boto3.client(
            service_name,
            region_name=self.region,
            aws_access_key_id=self.__access_key_id(),
            aws_secret_access_key=self.__secret_access_key(),
            aws_session_token=self.__session_token(),
            config=self.config
        )
        return client

    def assumed_role_resource(self, service_name):
        self.logger.debug(f"assumed_role_resource(self, {service_name})")

        resource = boto3.resource(
            service_name,
            region_name=self.region,
            aws_access_key_id=self.__access_key_id(),
            aws_secret_access_key=self.__secret_access_key(),
            aws_session_token=self.__session_token(),
            config=self.config
        )
        return resource

    def __access_key_id(self):
        return self.assumed_role_keys.get('AccessKeyId', None)

    def __secret_access_key(self):
        return self.assumed_role_keys.get('SecretAccessKey', None)

    def __session_token(self):
        return self.assumed_role_keys.get('SessionToken', None)


logging.getLogger(__name__).addHandler(logging. NullHandler())
