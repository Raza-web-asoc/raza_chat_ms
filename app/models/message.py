from pydantic import BaseModel


class MessageRequest(BaseModel):
    pets: list[int]
    pet_id: int
    message: str


