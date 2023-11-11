from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def status():
    """
    This endpoint is used for health metrics
    """
    return {"status": "ok"}
