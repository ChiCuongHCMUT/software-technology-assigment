from fastapi import APIRouter, Header
from models.room import CreateRoomRequest, UpdateRoomRequest


router = APIRouter(prefix="/room")


@router.post(
    "/",
)
async def create_room(
    create_room_request: CreateRoomRequest
):
    try:
        # Todo
        pass
    except Exception as e:
        raise e


@router.get(
    "/",
)
async def list_room(
):
    try:
        # Todo
        pass
    except Exception as e:
        raise e


@router.put(
    "/{room_id}",
)
async def update_room(
    update_room_request: UpdateRoomRequest,
):
    try:
        # Todo
        pass
    except Exception as e:
        raise e


@router.delete(
    "/{room_id}",
)
async def delete_room(
):
    try:
        # Todo
        pass
    except Exception as e:
        raise e


@router.post(
    "/checkin/{room_id}",
)
async def checkin_room(
    user_id: str = Header(..., description="User ID"),
    booking_id: str = Header(..., description="Booking ID"),
):
    try:
        # Todo
        pass
    except Exception as e:
        raise e


@router.post(
    "/checkout/{room_id}",
)
async def checkout_room(
    user_id: str = Header(..., description="User ID"),
    booking_id: str = Header(..., description="Booking ID"),
):
    try:
        # Todo
        pass
    except Exception as e:
        raise e