from beanie import Document
from typing import Optional
from datetime import datetime


class RoomHistory(Document):
    room_id: Optional[str] = None
    user_id: Optional[str] = None
    checkin_at: Optional[datetime] = None
    checkout_at: Optional[datetime] = None

    class Settings:
        name = "Room_History"

