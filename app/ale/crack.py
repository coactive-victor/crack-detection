from io import BytesIO

import cv2
import numpy as np
from fastapi import HTTPException, UploadFile


def load_image_from_upload(file: UploadFile) -> np.ndarray:
    """Loads an image from an uploaded file."""
    try:
        image_data = np.frombuffer(file.file.read(), np.uint8)
        image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Failed to decode the uploaded image.")
        return image
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")


def detect_edges(image: np.ndarray) -> np.ndarray:
    """Detects edges in the image using Canny Edge Detection."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, threshold1=50, threshold2=150)
    return edges


def highlight_edges(image: np.ndarray, edges: np.ndarray) -> np.ndarray:
    """Creates a highlighted version of the image where detected edges are marked in red."""
    mask = np.zeros_like(image)
    mask[edges != 0] = [0, 0, 255]  # Red color for highlighting
    highlighted_image = cv2.addWeighted(image, 0.65, mask, 0.35, 0)
    return highlighted_image


def convert_image_to_bytes(image: np.ndarray, format: str = ".jpg") -> BytesIO:
    """Converts an OpenCV image to a byte buffer."""
    success, buffer = cv2.imencode(format, image)
    if not success:
        raise ValueError("Failed to encode the image.")
    return BytesIO(buffer)
