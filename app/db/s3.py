import boto3

from app.settings import Settings


def get_s3_client():
    settings = Settings()
    session = boto3.Session(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
    s3_client = session.client("s3")
    yield s3_client
