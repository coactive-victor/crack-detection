from typing import Any

from pydantic import UUID4, BaseModel, Field

import app.routers.shared as cc


class DetectImageResponse(BaseModel):
    operation_id: UUID4 = Field(
        description="Unique identifier for the detection operation",
        example=cc.OPERATION_ID_EXAMPLE,
        nullable=False,
    )
    message: str = Field(
        description="Successful detection message",
        example="Images successfully processed and uploaded to S3.",
        nullable=False,
    )
    s3_uri: str = Field(
        description="URI of the uploaded images in S3",
        example=f"s3://{cc.BUCKET_NAME}/{cc.OUTBOUND_FOLDER}/{cc.OPERATION_ID_EXAMPLE}/",
        nullable=False,
    )
    images: list[str] = Field(
        description="List of images uploaded to S3",
        example=[],
        nullable=False,
    )

    @staticmethod
    def get_class_example():
        """Generate an example instance of the DetectImageResponse class."""
        return DetectImageResponse(
            operation_id=cc.OPERATION_ID_EXAMPLE,
            message="Images successfully processed and uploaded to S3.",
            s3_uri=f"s3://{cc.BUCKET_NAME}/{cc.OUTBOUND_FOLDER}/{cc.OPERATION_ID_EXAMPLE}/",
            images=[],
        )

    class Config:
        @staticmethod
        def json_schema_extra(schema: dict[str, Any], model: type["DetectImageResponse"]) -> None:
            schema["example"] = DetectImageResponse.get_class_example().dict()
