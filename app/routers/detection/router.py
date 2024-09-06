from uuid import uuid4

import cv2
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from mypy_boto3_s3 import S3Client

from app.ale.crack import (
    convert_image_to_bytes,
    detect_edges,
    highlight_edges,
    load_image_from_upload,
)
from app.db.s3 import get_s3_client
from app.routers.detection.schema import DetectImageResponse
from app.routers.detection.utils import is_image_file, upload_image_to_s3
from app.settings import Settings

router = APIRouter(prefix="/detection", tags=["detection"])

settings = Settings()


@router.post(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=DetectImageResponse,
    summary="Crack detection",
    description="Detect a crack in an image with computer vision",
)
async def detect_image(
    s3_client: S3Client = Depends(get_s3_client),
    file: UploadFile = File(...),
):
    operation_id = uuid4()

    print(f"Starting crack detection for operation {operation_id}")

    if not is_image_file(file):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image file")

    # Rewind file pointer after PIL read
    file.file.seek(0)

    # Load the image from the uploaded file
    image = load_image_from_upload(file)

    # Detect edges in the image
    edges = detect_edges(image)

    # Highlight edges on the original image
    highlighted_image = highlight_edges(image, edges)

    # Convert images to byte buffers
    original_image_data = convert_image_to_bytes(image=image, format=".png")
    edges_image_data = convert_image_to_bytes(image=cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR), format=".png")
    highlighted_image_data = convert_image_to_bytes(image=highlighted_image, format=".png")

    # Define bucket name and upload images to S3
    bucket_name = settings.BUCKET_NAME
    folder_name = f"{settings.OUTBOUND_FOLDER}/{operation_id}"
    s3_uri = f"s3://{bucket_name}/{folder_name}/"

    upload_image_to_s3(
        image_data=original_image_data,
        bucket_name=bucket_name,
        object_key=f"{folder_name}/original_image.png",
        s3_client=s3_client,
    )
    upload_image_to_s3(
        image_data=edges_image_data,
        bucket_name=bucket_name,
        object_key=f"{folder_name}/edges_image.png",
        s3_client=s3_client,
    )
    upload_image_to_s3(
        image_data=highlighted_image_data,
        bucket_name=bucket_name,
        object_key=f"{folder_name}/highlighted_crack.png",
        s3_client=s3_client,
    )

    return DetectImageResponse(
        operation_id=operation_id,
        message="Images successfully processed and uploaded to S3.",
        s3_uri=s3_uri,
    )
