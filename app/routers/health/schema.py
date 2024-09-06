from pydantic import BaseModel


class AliveResponse(BaseModel):
    status: str


class ReadyResponse(BaseModel):
    status: str
