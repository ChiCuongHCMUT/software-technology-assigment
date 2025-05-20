from fastapi import APIRouter, HTTPException, status
from models.internal_checkin import InternalCheckinRequest
from controller.internal_checkin_controller import handle_sqs_event
from dao.base import DBConnection


router = APIRouter(prefix="/internalCheckin")


@router.post(
    "/",
    response_model=None,
)
async def internal_checkin_device(
    device_uid: str,
    body: InternalCheckinRequest,
):
    try:
        conn = DBConnection.connect()
        response = handle_sqs_event(
            message=body.message,
            attributes=body.attributes,
            conn=conn,
            device_uid=device_uid
        )
        if response:
            return response
        return {"status": "Checkin Successfully!"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        DBConnection.close()

