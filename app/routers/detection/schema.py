from pydantic import BaseModel


class DetectImageResponse(BaseModel):
    message: str
    s3_uri: str
