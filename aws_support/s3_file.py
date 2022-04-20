import logging
from pathlib import Path
from botocore.errorfactory import ClientError

S3Client = object


class S3File:
    DOWNLOAD_DIRECTORY = "./download/"

    def __init__(self, client, bucket_name, key, logger_name):
        self.client: S3Client = client
        self.bucket_name = bucket_name
        self.key = key
        self.logger = logging.getLogger(logger_name)

    def exists(self):
        self.logger.debug(f"exists()")
        try:
            self.client.head_object(Bucket=self.bucket_name, Key=self.key)
            found = True
        except ClientError:
            found = False

        return found

    def copy_to_local(self, file_name):
        self.logger.debug(f"copy_to_local()")

        self.__create_download_dir()
        path_name = self.DOWNLOAD_DIRECTORY + file_name
        self.client.download_file(self.bucket_name, self.key, path_name)

    def __create_download_dir(self):
        self.logger.debug(f"_create_download_dir()")

        Path(self.DOWNLOAD_DIRECTORY).mkdir(exist_ok=True)

    def __delete_local_file(self, file_name):
        self.logger.debug(f"_delete_download_dir()")

        # shutil.rmtree(DOWNLOAD_DIRECTORY, ignore_errors=True)


logging.getLogger(__name__).addHandler(logging.NullHandler())
