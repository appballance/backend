import os
import boto3

from dotenv import load_dotenv

from balance_service.interfaces.boto_s3 import BasicBotoS3

from balancelib.interactors.response_api_interactor import ResponseError


class BotoS3Interactor(BasicBotoS3):
    def __init__(self):
        self.load_dotenv()

        self.region_name = os.environ['AWS_S3_REGION_NAME']
        self.aws_access_key_id = os.environ['AWS_S3_KEY_ID']
        self.aws_secret_access_key = os.environ['AWS_S3_KEY']

        self.service = boto3
        self.s3 = None
        self.authenticate()

    @staticmethod
    def load_dotenv():
        load_dotenv()

    """
        This method be authenticated in s3 before of use the call the methods.
    """
    def authenticate(self):
        try:
            self.s3 = self.service.resource(
                service_name="s3",
                region_name=self.region_name,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key, )

            if list(self.s3.buckets.all()):
                return True
            else:
                return False
        except:
            raise ResponseError(
                status_code=400,
                message="failed in authenticated of S3 instance",
            )

    """
        bucket_name: This key represent the name of bucket.
        file_path: This key represent the name or/and path of current file.
        file_path_new: This key represent the name or/and path of new file.
    """
    def upload_file(self,
                    bucket_name: str,
                    file_path: str,
                    file_path_new: str):
        self.s3.Bucket(bucket_name) \
            .upload_file(
                Key=file_path_new,
                Filename=file_path,)

    """
        bucket_name: This key represent the name of bucket.
        file_path: This key represent the name or/and path of current file.
        file_path_new: This key represent the name or/and path of new file.
    """
    def download_file(self,
                      bucket_name: str,
                      file_path: str,
                      file_path_new: str):
        try:
            self.s3.Bucket(bucket_name) \
                .download_file(
                    Key=file_path,
                    Filename=file_path_new,)
        except:
            raise ResponseError(
                status_code=400,
                message=f"failed download S3 file {file_path}",
            )

    """
        bucket_name: This key represent the name of bucket.
        file_path: This key represent the name or/and path of current file.
    """
    def has_file(self,
                 bucket_name: str,
                 file_path: str):
        try:
            file = self.s3.Bucket(bucket_name).Object(file_path).get()

            if file['Body']:
                return True
            else:
                print('ERROR - file dont exists: ', file_path)

                return False
        except:
            print('ERROR - failed in get object in S3')
            return False
