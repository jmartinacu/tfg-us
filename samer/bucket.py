import boto3
from django.conf import settings

s3 = boto3.client("s3")


def upload_file(file: bytes, object_name: str):
    bucket = settings.AWS_BUCKET_NAME
    region = settings.AWS_DEFAULT_REGIO
    s3.upload_fileobj(file, bucket, object_name)
    return f"https://{bucket}.s3.{region}.amazonaws.com/{object_name}"


def delete_file(object_name: str):
    bucket = settings.AWS_BUCKET_NAME
    s3.delete_object(Bucket=bucket, Key=object_name)
