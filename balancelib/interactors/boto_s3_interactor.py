import os

import boto3
from dotenv import load_dotenv

from balance_service.interfaces.boto_s3 import BasicBotoS3


class BotoS3Interactor(BasicBotoS3):
    def __init__(self):
        self.load_dotenv()

        self.bucket_path = os.environ['AWS_BUCKET_NAME']
        self.region_name = os.environ['AWS_REGION_NAME']
        self.aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
        self.aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']

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
            return False

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
