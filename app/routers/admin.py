from fastapi import APIRouter, Depends
from app.dependencies import require_admin_or_superadmin


admin_router = APIRouter(prefix="/admin",
                         dependencies=[Depends(require_admin_or_superadmin)])

@admin_router.get("/test_router")
async def check_admin_rights():
    return {"message": "ok"}
