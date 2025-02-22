import os
import subprocess
from io import BytesIO

import boto3
from django.conf import settings

s3 = boto3.client("s3")


def upload_file(file: bytes, object_name: str):
    bucket = settings.AWS_BUCKET_NAME
    region = settings.AWS_DEFAULT_REGION
    s3.upload_fileobj(file, bucket, object_name)
    return f"https://{bucket}.s3.{region}.amazonaws.com/{object_name}"


def delete_file(object_name: str):
    bucket = settings.AWS_BUCKET_NAME
    s3.delete_object(Bucket=bucket, Key=object_name)


def upload_thumbnail(frame: int, video_url: str):
    command = [
        "ffmpeg",
        "-i",
        video_url,
        "-vf",
        f"select='eq(n,{frame})'",
        "-q:v",
        "3",
        "-f",
        "image2pipe",
        "-vcodec",
        "mjpeg",
        "pipe:1",
    ]
    process = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
    )
    if process.returncode != 0:
        raise Exception(f"ffmpeg error: {process.stderr.decode('utf-8')}")
    video_name = video_url.split("/")[-1]
    thumb_name, _thumb_ext = os.path.splitext(video_name)
    thumb_io = BytesIO(process.stdout)
    thumbnail_url = upload_file(
        file=thumb_io, object_name=f"videos/thumbnails/{thumb_name}.jpg"
    )
    return thumbnail_url
