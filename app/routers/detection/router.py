from fastapi import APIRouter, Depends, status
from mypy_boto3_s3 import S3Client  # Import type hint for S3 client
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.db.s3 import get_s3_client

router = APIRouter(prefix="/detection", tags=["detection"])


@router.post(
    path="/",
    status_code=status.HTTP_202_ACCEPTED,
)
def create_user(
    session: Session = Depends(get_session),
    s3_client: S3Client = Depends(get_s3_client),
):
    return {"message": "Hello, World!"}
