from fastapi import FastAPI

from app.routers.detection.router import router as detection_router

app = FastAPI()

app.include_router(detection_router)
