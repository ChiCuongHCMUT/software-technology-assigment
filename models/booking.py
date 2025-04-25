from beanie import Document
from pydantic import BaseModel
from typing import Optional

class CreateBookingRequest(BaseModel):
    room_id: str
    user_id: str
    quantity: int
    purpose: str
    time_start: int
    time_end: int
    date: str


class UpdateBookingRequest(BaseModel):
    room_id: Optional[str] = None
    user_id: Optional[str] = None
    quantity: Optional[int] = None
    purpose: Optional[str] = None
    time_start: Optional[int] = None
    time_end: Optional[int] = None
    date: Optional[str] = None
    status: Optional[str] = None


class Booking(Document):
    booking_id: Optional[str] = None
    room_id: Optional[str] = None
    user_id: Optional[str] = None
    quantity: Optional[int] = None
    purpose: Optional[str] = None
    time_start: Optional[int] = None
    time_end: Optional[int] = None
    date: Optional[str] = None
    status: Optional[str] = None

    class Settings:
        name = "Booking"

