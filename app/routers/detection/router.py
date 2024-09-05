from fastapi import APIRouter, status

router = APIRouter(prefix="/detection", tags=["detection"])


@router.post(
    path="/",
    status_code=status.HTTP_202_ACCEPTED,
)
def create_user():
    return {"message": "Hello, World!"}
