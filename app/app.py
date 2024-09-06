from fastapi import FastAPI

from app.routers.detection.router import router as detection_router
from app.routers.health.router import router as health_router

app = FastAPI()

app.include_router(health_router)
app.include_router(detection_router)
