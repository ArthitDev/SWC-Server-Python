from fastapi import APIRouter, Depends
from app.middlewares.authMiddleware import get_current_user
from app.schemas.login_admin import AdminLoginResponse

router = APIRouter()


@router.get("/admin", response_model=AdminLoginResponse)
async def read_protected_route(
    current_user=Depends(get_current_user),
):
    return {
        "message": "คุณเข้าถึงข้อมูลที่ป้องกันไว้ได้",
    }
