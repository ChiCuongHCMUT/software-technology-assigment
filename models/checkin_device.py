from pydantic import BaseModel
from typing import Optional

class DeviceCheckinRequest(BaseModel):
    pass

class DeviceCheckinResponse(BaseModel):
    isBase64Encoded: Optional[bool] = None
    statusCode: Optional[int] = None
    body: Optional[dict] = None



