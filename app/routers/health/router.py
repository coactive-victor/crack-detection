from fastapi import APIRouter

from app.routers.health.schema import AliveResponse, ReadyResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/alive", response_model=AliveResponse)
async def alive() -> AliveResponse:
    return AliveResponse(status="ok")


@router.get("/ready", response_model=ReadyResponse)
async def ready() -> ReadyResponse:
    return ReadyResponse(status="ok")
