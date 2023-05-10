from unittest.mock import MagicMock

from pytest import fixture

from balancelib.interactors.boto_s3_interactor import (
    BotoS3Interactor,
    BotoS3RequestModel,
)


@fixture
def interactor_factory():
    def request_interactor(mock_request=MagicMock(),
                           mock_service=MagicMock()):
        return BotoS3Interactor(mock_request,
                                mock_service)

    return request_interactor


def test_boto_s3_request_model():
    mock_region_name = MagicMock()
    mock_aws_access_key_id = MagicMock()
    mock_aws_secret_access_key = MagicMock()

    response = BotoS3RequestModel(
        mock_region_name,
        mock_aws_access_key_id,
        mock_aws_secret_access_key, )

    assert response.region_name == mock_region_name
    assert response.aws_access_key_id == mock_aws_access_key_id
    assert response.aws_secret_access_key == mock_aws_secret_access_key


def test_boto_s3_interactor(interactor_factory):
    mock_request = MagicMock()
    mock_service = MagicMock()

    interactor = interactor_factory(mock_request,
                                    mock_service, )

    assert interactor.request == mock_request
    assert interactor.service == mock_service


patch_root = 'balancelib.interactors.boto_s3_interactor'


def test_boto_s3_interactor_authenticate(interactor_factory):
    interactor = interactor_factory()

    result = interactor.authenticate()

    mock_instance = interactor.service.resource(
        service_name="s3",
        region_name=interactor.request.region_name,
        aws_access_key_id=interactor.request.aws_access_key_id,
        aws_secret_access_key=interactor.request.aws_secret_access_key,
    )

    mock_result = True if list(mock_instance.instance.buckets.all()) else False

    assert result == mock_result


def test_boto_s3_interactor_upload_file(interactor_factory):
    mock_bucket_name = MagicMock()
    mock_file_path = MagicMock()
    mock_file_path_new = MagicMock()

    interactor = interactor_factory()

    interactor.upload_file(
        mock_bucket_name,
        mock_file_path,
        mock_file_path_new
    )


def test_boto_s3_interactor_download_file(interactor_factory):
    mock_bucket_name = MagicMock()
    mock_file_path = MagicMock()
    mock_file_path_new = MagicMock()

    interactor = interactor_factory()

    interactor.download_file(
        mock_bucket_name,
        mock_file_path,
        mock_file_path_new
    )


def test_boto_s3_interactor_has_file(interactor_factory):
    mock_bucket_name = MagicMock()
    mock_file_path = MagicMock()

    interactor = interactor_factory()

    interactor.has_file(
        mock_bucket_name,
        mock_file_path,
    )
