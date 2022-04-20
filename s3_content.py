#!/usr/bin/env python3
import json
import logging
import zipfile
import mimetypes
import time
import constants
import boto3
import common as common
import aws_support.string_utils as su
from aws_support import S3File

logging.basicConfig(format='%(asctime)s [%(levelname)5s] - %(message)s',
                    # datefmt='%Y-%m-%dT%H:%M:%S%z',
                    level=logging.INFO)
logger = logging.getLogger(constants.LOGGER_NAME)


def _download_website_zipfile(**args):
    logger.debug(f"_download_website_zipfile({args})")
    source_client = args['client']
    source_bucket = args['bucket']
    source_key = args['key']
    source_file = S3File(source_client, source_bucket, source_key,
                         constants.LOGGER_NAME)
    file_name = constants.ZIPFILE_NAME
    source_file.copy_to_local(file_name)
    return f"{S3File.DOWNLOAD_DIRECTORY}/{file_name}"


def _create_website_bucket_name(args):
    logger.debug(f"_create_website_bucket_name({args})")
    bucket_name = su.replace_project(constants.WEBSITE_BUCKET, args['project'])
    bucket_name = su.replace_env(bucket_name, args['env'])
    bucket_name = su.replace_region(bucket_name, args['region'])
    bucket_name = su.replace_app(bucket_name, args['app'])
    return bucket_name


def _delete_target_s3_content(args):
    logger.debug(f"_delete_target_s3_content({args})")

    # used a Resource/Bucket rather than the Client to simplify file deletion
    #  a Bucket object handles retrieving all of the files much easier
    resource = common.AWS_CLIENT.assumed_role_resource('s3')
    bucket_name = _create_website_bucket_name(args)
    logger.info(f"Deleting content on website S3 bucket: {bucket_name}")

    bucket = resource.Bucket(bucket_name)
    bucket.objects.all().delete()


def _upload_website_content(args, zipfile_name):
    logger.debug(f"_upload_website_content({args}, {zipfile_name})")
    client = common.AWS_CLIENT.assumed_role_client('s3')
    bucket = _create_website_bucket_name(args)

    logger.info(f"Uploading content to website S3 bucket: {bucket}")

    zf = zipfile.ZipFile(zipfile_name)
    for filename in zf.namelist():
        content_type = mimetypes.guess_type(filename)[0]
        # if filename == 'config.json':
        #     continue
        if not content_type:
            content_type = 'text/plain'
        logger.info("uploadling " + filename)
        client.upload_fileobj(zf.open(filename), Bucket=bucket, Key=filename,
                              ExtraArgs={'ContentType': content_type})


def _verify_zip_exists(args):
    logger.debug(f"verify_zip_exists({args})")

    logger.info(f"Verifying Application: {args['app']},"
                f" Version: {args['version']} exists")

    bucket_name = args['data']['inputArtifacts'][0]['s3Location']['bucketName']
    key = args['data']['inputArtifacts'][0]['s3Location']['objectKey']
    print(bucket_name, key)
    client = common.AWS_CLIENT.client('s3')
    s3_file = S3File(client, bucket_name, key, constants.LOGGER_NAME)
    if not s3_file.exists():
        raise Exception(f"Application: {args['app']},"
                        f" Version: {args['version']} does NOT exist")


def lambda_handler(event, context):
    """
    Deploys the static web site to the selected account/region
    """
    args = event['CodePipeline.job']['data']
    job_id = event['CodePipeline.job']['id']
    artifacts = args['inputArtifacts']
    cred = args['artifactCredentials']

    key_id = cred['accessKeyId']
    key_secret = cred['secretAccessKey']
    session_token = cred['sessionToken']

    s3 = boto3.client('s3', aws_access_key_id=key_id,
                      aws_secret_access_key=key_secret,
                      aws_session_token=session_token)

    zip = _download_website_zipfile(
        client=s3,
        bucket=artifacts[0]['location']['s3Location']['bucketName'],
        key=artifacts[0]['location']['s3Location']['objectKey']
    )

    # try:
    zf = zipfile.ZipFile(zip)
    config = zf.open('config.json').read().decode()
    args = json.loads(config)
    args['env'] = 'dev'
    args['region'] = 'us-east-1'
    print(args)
    logger.setLevel(logging.DEBUG) if args['debug'] else None

    info = common.run_info(args)
    common.setup_aws_client(args)
    logger.debug(f"deploy({args})")

    # _verify_zip_exists(args)
    _delete_target_s3_content(args)
    _upload_website_content(args, zip)
    info['Status'] = 'Pass'

    # except Exception as ex:
    #     logger.error(f"deploy threw an exception: {ex}")
    #     code_pipline = boto3.client('codepipeline', aws_access_key_id=key_id,
    #                                 aws_secret_access_key=key_secret,
    #                                 aws_session_token=session_token)
    #     code_pipline.put_job_failure_result(jobId=job_id,  failureDetails={
    #                                         'message': str(ex), 'type': 'JobFailed'})
    #     exit(1)
    # else:
    #     code_pipline = boto3.client('codepipeline', aws_access_key_id=key_id,
    #                                 aws_secret_access_key=key_secret,
    #                                 aws_session_token=session_token)
    #     code_pipline.put_job_success_result(jobId=job_id)
    # finally:
    #     info['Duration'] = int(time.time() * 1000) - info['Duration']
    # print(f"\nJob Execution Status:  {info}")
    # logger.info(f"Exiting")


if __name__ == '__main__':
    lambda_handler(json.loads(open("demo.json").read()), {})
