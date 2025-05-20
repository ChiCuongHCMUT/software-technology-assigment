from fastapi import APIRouter, HTTPException, status
from controller.extenal_checkin_controller import device_enroll_controller
from models.enroll_device import DeviceEnrollRequest, DeviceEnrollResponse
import constants as const
import copy


router = APIRouter(prefix="/v2/enrol")


@router.post(
    "/",
    response_model=DeviceEnrollResponse,
)
async def checkin_device(
    body: DeviceEnrollRequest
):
    try:
        event = copy.deepcopy(const.CheckinEvent.INIT_EVENT)
        event['body'] = body.dict()

        enroll_response = device_enroll_controller(event)
        return DeviceEnrollResponse(**enroll_response)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))