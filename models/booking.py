from beanie import Document
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CreateBookingRequest(BaseModel):
    room_id: str
    user_id: str
    quantity: int
    purpose: str
    time_start: datetime
    time_end: datetime


class UpdateBookingRequest(BaseModel):
    room_id: Optional[str] = None
    user_id: Optional[str] = None
    quantity: Optional[int] = None
    purpose: Optional[str] = None
    time_start: Optional[datetime] = None
    time_end: Optional[datetime] = None
    status: Optional[str] = None


class Booking(Document):
    booking_id: Optional[str] = None
    room_id: Optional[str] = None
    user_id: Optional[str] = None
    quantity: Optional[int] = None
    purpose: Optional[str] = None
    time_start: Optional[datetime] = None
    time_end: Optional[datetime] = None
    status: Optional[str] = None

    class Settings:
        name = "Booking"

