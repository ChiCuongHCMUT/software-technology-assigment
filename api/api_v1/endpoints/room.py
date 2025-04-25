from fastapi import APIRouter, Header, HTTPException
from models.room import CreateRoomRequest, UpdateRoomRequest, Room
from models.booking import Booking
from const import RoomState
from typing import List


router = APIRouter(prefix="/room")


@router.post(
    "/",
    response_model=Room
)
async def create_room(
    create_room_request: CreateRoomRequest
):
    try:
        # Create new room with initial state as AVAILABLE
        room = Room(
            **create_room_request.dict(),
            room_state=RoomState.AVAILABLE
        )
        await room.save()
        return room
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/",
    response_model=List[Room]
)
async def list_room():
    try:
        # Get all rooms
        rooms = await Room.find_all().to_list()
        return rooms
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/schedules"
)
async def get_room_schedules(
    date: str = Header(..., description="Date in YYYY-MM-DD format"),
):
    try:
        rooms = await Room.find_all().to_list()
        room_schedules = []
        for room in rooms:
            room_schedule = {
                "room_id": room.room_id,
                "status": [RoomState.AVAILABLE, RoomState.AVAILABLE, RoomState.AVAILABLE, RoomState.AVAILABLE, RoomState.AVAILABLE, RoomState.AVAILABLE, RoomState.AVAILABLE, RoomState.AVAILABLE, RoomState.AVAILABLE, RoomState.AVAILABLE, RoomState.AVAILABLE, RoomState.AVAILABLE,],
            }
            bookings = await Booking.find(Booking.room_id == room.room_id, Booking.date == date).to_list()
            if bookings:
                for booking in bookings:
                    start_time = int(booking.time_start)
                    end_time = int(booking.time_end)
                    for i in [start_time, end_time]:
                        room_schedule["status"][i] = RoomState.BOOKED
            current_room = await Room.find_one(Room.room_id == room.room_id)
            if current_room.room_state == RoomState.IN_USE:
                for booking in bookings:
                    if booking.booking_id == current_room.current_reserved_by_booking_id:
                        start_time = int(booking.time_start)
                        end_time = int(booking.time_end)
                        for i in [start_time, end_time]:
                            room_schedule["status"][i] = RoomState.IN_USE
            room_schedules.append(room_schedule)
        return room_schedules
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put(
    "/{room_id}",
    response_model=Room
)
async def update_room(
    room_id: str,
    update_room_request: UpdateRoomRequest,
):
    try:
        # Get room by ID
        room = await Room.get(room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")

        # Update room with new data
        update_data = update_room_request.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(room, key, value)

        await room.save()
        return room
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete(
    "/{room_id}",
    response_model=dict
)
async def delete_room(
    room_id: str
):
    try:
        # Get room by ID
        room = await Room.get(room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")

        # Delete room
        await room.delete()
        return {"message": "Room deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/checkin/{room_id}",
    response_model=Room
)
async def checkin_room(
    room_id: str,
    user_id: str = Header(..., description="User ID"),
    booking_id: str = Header(..., description="Booking ID"),
):
    try:
        # Get room by ID
        room = await Room.find_one(Room.room_id == room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")

        # Check if room is available
        if room.room_state != RoomState.AVAILABLE:
            raise HTTPException(status_code=400, detail="Room is not available for check-in")

        # Update room state to IN_USE
        room.room_state = RoomState.IN_USE
        room.current_reserved_by_user_id = user_id
        room.current_reserved_by_booking_id = booking_id
        await room.save()
        return room
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/checkout/{room_id}",
    response_model=Room
)
async def checkout_room(
    room_id: str,
    user_id: str = Header(..., description="User ID"),
    booking_id: str = Header(..., description="Booking ID"),
):
    try:
        # Get room by ID
        room = await Room.find_one(Room.room_id == room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")

        # Check if room is in use
        if room.room_state != RoomState.IN_USE:
            raise HTTPException(status_code=400, detail="Room is not in use")

        if room.current_reserved_by_user_id != user_id:
            raise HTTPException(status_code=400, detail="User ID does not match current reservation")
        if room.current_reserved_by_booking_id != booking_id:
            raise HTTPException(status_code=400, detail="Booking ID does not match current reservation")

        # Update room state to AVAILABLE
        room.room_state = RoomState.AVAILABLE
        room.current_reserved_by_user_id = None
        room.current_reserved_by_booking_id = None
        await room.save()
        return room
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))