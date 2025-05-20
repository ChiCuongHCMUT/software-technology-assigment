from fastapi import APIRouter
from .endpoints.internal_checkin_device import router as internal_checkin_router
from .endpoints.enroll_device import router as enroll_router
from .endpoints.checkin_device import router as checkin_router

router = APIRouter()
router.include_router(checkin_router, tags=["Device Checkin"])
router.include_router(enroll_router, tags=["Device Enroll"])
router.include_router(internal_checkin_router, tags=["Internal Checkin Device"])
