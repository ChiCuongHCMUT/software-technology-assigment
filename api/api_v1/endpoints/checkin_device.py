from fastapi import APIRouter, Header, HTTPException, status
from models.checkin_device import DeviceCheckinRequest, DeviceCheckinResponse
from controller.extenal_checkin_controller import device_checkin_controller
import constants as const
import copy


router = APIRouter(prefix="/v3/checkin")

@router.post(
    "/",
    response_model=DeviceCheckinResponse,
)
async def checkin_device(
    body: DeviceCheckinRequest,
    Authorization: str = Header(...),
):
    try:
        event = copy.deepcopy(const.CheckinEvent.INIT_EVENT)
        event['headers']['Authorization'] = Authorization
        event['body'] = body.dict()

        checkin_response = device_checkin_controller(event)
        return DeviceCheckinResponse(**checkin_response)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))