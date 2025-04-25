from fastapi import APIRouter, HTTPException
from models.booking import CreateBookingRequest, UpdateBookingRequest, Booking
from models.room import Room
from const import RoomState, BookingState
from typing import List
import random


router = APIRouter(prefix="/booking")


@router.post(
    "/{room_id}",
    response_model=Booking
)
async def create_booking_room(
    room_id: str,
    create_booking_request: CreateBookingRequest,
):
    try:
        # Get room and check if it's available
        room = await Room.find_one(Room.room_id == room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")

        if room.room_state != RoomState.AVAILABLE:
            raise HTTPException(status_code=400, detail="Room is not available for booking")

        # Create new booking
        booking = Booking(
            **create_booking_request.dict(),
            booking_id=str(random.randint(1000000, 9999999)),
            status=BookingState.COMPLETED,
        )
        await booking.save()
        return booking
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put(
    "/{booking_id}",
    response_model=Booking
)
async def update_booking_room(
    booking_id: str,
    update_booking_request: UpdateBookingRequest,
):
    try:
        # Get booking by ID
        booking = await Booking.find_one(Booking.booking_id == booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        # Update booking with new data
        update_data = update_booking_request.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(booking, key, value)

        await booking.save()
        return booking
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/{room_id}",
    response_model=List[Booking]
)
async def get_list_booking_of_room(
    room_id: str
):
    try:
        # Get all bookings for specific room
        bookings = await Booking.find({"room_id": room_id}).to_list()
        return bookings
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))