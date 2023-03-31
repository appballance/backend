import os

import boto3
from dotenv import load_dotenv

from balance_service.interfaces.boto_s3 import BasicBotoS3

from balancelib.interactors.response_api_interactor import ResponseError


class BotoS3Interactor(BasicBotoS3):
    def __init__(self, bucket_name: str):
        self.load_dotenv()

        self.bucket_path = bucket_name
        self.region_name = os.environ['AWS_S3_REGION_NAME']
        self.aws_access_key_id = os.environ['AWS_S3_KEY_ID']
        self.aws_secret_access_key = os.environ['AWS_S3_KEY']

        self.service = boto3
        self.s3 = None
        self.authenticate()

    @staticmethod
    def load_dotenv():
        load_dotenv()

    def authenticate(self,):
        self.s3 = self.service.resource(
            service_name="s3",
            region_name=self.region_name,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,)

        try:
            list(self.s3.buckets.all())
            return True
        except:
            raise ResponseError(status_code=400,
                                message="failed in authenticated of S3 instance")

    def upload_file(self,
                    file_path: str,
                    file_path_new: str):
        self.s3.Bucket(self.bucket_path)\
            .upload_file(Key=file_path, Filename=file_path_new,)

    def download_file(self,
                      file_path: str,
                      file_path_new: str):
        self.s3.Bucket(self.bucket_path)\
            .download_file(Key=file_path, Filename=file_path_new,)

    def has_file(self, file_path: str):
        try:
            file = self.s3.Bucket(self.bucket_path).Object(file_path).get()

            if file['Body']:
                return True
            return False
        except:
            print('Error: file dont exists: ', file_path)
            return False
