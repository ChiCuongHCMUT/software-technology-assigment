from pydantic import BaseModel
from typing import Optional

class DeviceEnrollRequest(BaseModel):
    pass

class DeviceEnrollResponse(BaseModel):
    isBase64Encoded: Optional[bool] = None
    statusCode: Optional[int] = None
    body: Optional[dict] = None



