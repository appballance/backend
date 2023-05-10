import boto3

from balance_service.interfaces.boto_s3 import BasicBotoS3

from balancelib.interactors.response_api_interactor import ResponseError


class BotoS3RequestModel:
    def __init__(self,
                 region_name: str,
                 aws_access_key_id: str,
                 aws_secret_access_key: str):
        self.region_name = region_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key


class BotoS3Interactor(BasicBotoS3):
    def __init__(self,
                 request: BotoS3RequestModel,
                 service: boto3):
        self.request = request
        self.service = service

        self.instance = None

        self.authenticate()

    """
        This method be authenticated in s3 before of use the call the methods.
    """
    def authenticate(self):
        try:
            self.instance = self.service.resource(
                service_name="s3",
                region_name=self.request.region_name,
                aws_access_key_id=self.request.aws_access_key_id,
                aws_secret_access_key=self.request.aws_secret_access_key, )

            result = True if list(
                self.instance.buckets.all()) else False
            return result
        except Exception:
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
        self.instance.Bucket(bucket_name) \
            .upload_file(
            Key=file_path_new,
            Filename=file_path, )

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
            self.instance.Bucket(bucket_name) \
                .download_file(
                Key=file_path,
                Filename=file_path_new, )
        except Exception:
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
            file = self.instance.Bucket(bucket_name).Object(file_path).get()

            if file['Body']:
                return True
            else:
                print('ERROR - file dont exists: ', file_path)

                return False
        except Exception:
            print('ERROR - failed in get object in S3')
            return False
