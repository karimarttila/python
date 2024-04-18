import boto3
import pytest
from moto import mock_aws
from pathlib import Path

@pytest.fixture(name="s3_client", scope="function")
def _s3_client():
    with mock_aws():
        yield boto3.client("s3", region_name="us-east-1")


@pytest.fixture(name="bucket_name", scope="function")
def _process_objects_bucket_name(s3_client):
    bucket_name = "some-bucket"
    s3_client.create_bucket(Bucket=bucket_name)
    return bucket_name


def get_test_file_path(filename: str) -> Path:
    file_path = Path(__file__).parent / "data" / filename
    if not file_path.exists():
        raise FileNotFoundError(f"File {file_path} not found")
    return file_path


def add_object_to_unprocessed_prefix(my_s3_client, bucket_name, file_name):
    unprocessed_key = f"unprocessed/{file_name}"
    test_file_path = get_test_file_path(file_name)
    my_s3_client.upload_file(test_file_path, bucket_name, unprocessed_key)


def test_process_object_happy_day_scenario(s3_client, bucket_name):
    bucket = bucket_name
    test_file_name = "object1.txt"
    unprocessed_key = f"unprocessed/{test_file_name}"
    processed_key = f"processed/{test_file_name}"
    add_object_to_unprocessed_prefix(s3_client, bucket, test_file_name)
    # Verify we have the object in the unprocessed prefix now.
    assert s3_client.head_object(Bucket=bucket, Key=unprocessed_key) is not None
    # Verify the object is not in the processed prefix yet.
    with pytest.raises(s3_client.exceptions.ClientError):
        s3_client.head_object(Bucket=bucket, Key=processed_key)
    # Use our application logic to process the object.
    from bucket.process_object import process_object
    process_object(bucket, unprocessed_key)
    # Verify the object is not in the unprocessed prefix any more.
    with pytest.raises(s3_client.exceptions.ClientError):
        s3_client.head_object(Bucket=bucket, Key=unprocessed_key)
    # Verify we have the object in the processed prefix now.
    assert s3_client.head_object(Bucket=bucket, Key=processed_key) is not None

def test_process_object_failed_scenario(s3_client, bucket_name):
    bucket = bucket_name
    test_file_name = "fail1.txt"
    unprocessed_key = f"unprocessed/{test_file_name}"
    processed_key = f"processed/{test_file_name}"
    add_object_to_unprocessed_prefix(s3_client, bucket, test_file_name)
    # Verify we have the object in the unprocessed prefix now.
    assert s3_client.head_object(Bucket=bucket, Key=unprocessed_key) is not None
    # Verify the object is not in the processed prefix yet.
    with pytest.raises(s3_client.exceptions.ClientError):
        s3_client.head_object(Bucket=bucket, Key=processed_key)
    # Use our application logic to process the object.
    from bucket.process_object import process_object
    # Test that the processing fails.
    with pytest.raises(ValueError, match=f"Some error occurred processing the object: {unprocessed_key}"):
        process_object(bucket, unprocessed_key)
    # Verify the object is still in the unprocessed prefix since the processing failed.
    assert s3_client.head_object(Bucket=bucket, Key=unprocessed_key) is not None    
    # Verify the object is not moved into the processed prefix since the processing failed.
    with pytest.raises(s3_client.exceptions.ClientError):
        s3_client.head_object(Bucket=bucket, Key=processed_key)


def test_process_object_does_not_exist_scenario(s3_client, bucket_name):
    bucket = bucket_name
    test_file_name = "not-exists1.txt"
    unprocessed_key = f"unprocessed/{test_file_name}"
    # Use our application logic to process the object.
    from bucket.process_object import process_object
    # Test that the processing fails since the object does not exist in the bucket and key.
    with pytest.raises(ValueError, match=f"Object {unprocessed_key} not found in bucket {bucket}"):
        process_object(bucket, unprocessed_key)


