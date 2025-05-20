from pydantic import BaseModel
from typing import Optional

class InternalCheckinRequest(BaseModel):
    message: Optional[dict] = None
    attributes: Optional[dict] = None



