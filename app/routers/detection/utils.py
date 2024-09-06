import io

from fastapi import UploadFile
from PIL import Image

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/gif"}


def is_image_file(file: UploadFile) -> bool:
    # Check file extension
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        return False

    # Check content type
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        return False

    try:
        image = Image.open(io.BytesIO(file.file.read()))
        image.verify()  # Verify if the file is indeed an image
    except (IOError, SyntaxError):
        return False

    return True
