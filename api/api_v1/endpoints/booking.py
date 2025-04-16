from fastapi import APIRouter
from models.booking import CreateBookingRequest, UpdateBookingRequest


router = APIRouter(prefix="/booking")


@router.post(
    "/{room_id}",
)
async def create_booking_room(
    create_booking_request: CreateBookingRequest,
):
    try:
        # Todo
        pass
    except Exception as e:
        raise e


@router.put(
    "/cancel/{booking_id}",
)
async def update_booking_room(
    update_booking_request: UpdateBookingRequest,
):
    try:
        # Todo
        pass
    except Exception as e:
        raise e


@router.get(
    "/{room_id}",
)
async def get_list_booking_of_room(
):
    try:
        # Todo
        pass
    except Exception as e:
        raise e