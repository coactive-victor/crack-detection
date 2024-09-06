from uuid import uuid4

from fastapi import APIRouter, Depends, File, UploadFile, status
from mypy_boto3_s3 import S3Client
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.db.s3 import get_s3_client
from app.settings import Settings

router = APIRouter(prefix="/detection", tags=["detection"])

settings = Settings()


@router.post(
    path="/",
    status_code=status.HTTP_202_ACCEPTED,
)
async def detect_image(
    session: Session = Depends(get_session),
    s3_client: S3Client = Depends(get_s3_client),
    file: UploadFile = File(...),
):
    image_id = uuid4()

    # Get the file's content and metadata
    file_content = await file.read()
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{image_id}.{file_extension}"
    content_type = file.content_type

    inbound_folder = settings.INBOUND_FOLDER
    s3_path = f"{inbound_folder}/{unique_filename}"
    s3_client.put_object(
        Bucket=settings.BUCKET_NAME,
        Key=s3_path,
        Body=file_content,
        ContentType=content_type,
    )

    return {"message": "File uploaded successfully", "filename": unique_filename}
