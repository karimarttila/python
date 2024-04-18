import boto3
from botocore.exceptions import ClientError

s3_client = boto3.client("s3")


def _check_object(bucket: str, key: str) -> bool:
    """Check if the object exists in the bucket."""
    try:
        s3_client.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError:
        return False


def _some_application_logic_with_the_object(bucket: str, key: str):
    """Process the object in the bucket."""
    # Here we would add the code to do some application logic with the object,
    # in this demo just print a message.
    print(f"Processing object {key} in bucket {bucket}")
    # Simulate that the object processing failed for a specific key.
    if "fail" in key:
        raise ValueError(f"Some error occurred processing the object: {key}")


def _move_object_to_processed(bucket: str, key: str):
    """Move the object from the unprocessed/ prefix to the processed/ prefix."""
    copy_source = {"Bucket": bucket, "Key": key}
    processed_key = key.replace("unprocessed/", "processed/")
    s3_client.copy_object(CopySource=copy_source,
                          Bucket=bucket,
                          Key=processed_key)
    s3_client.delete_object(Bucket=bucket, Key=key)


def process_object(bucket: str, key: str):
    """ Main entry point to the module to process the object in the bucket."""
    if not _check_object(bucket, key):
        raise ValueError(f"Object {key} not found in bucket {bucket}")
    _some_application_logic_with_the_object(bucket, key)
    _move_object_to_processed(bucket, key)
