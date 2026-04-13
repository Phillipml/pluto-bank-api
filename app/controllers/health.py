from fastapi import APIRouter


router = APIRouter(prefix="/health")


@router.get("/")
def health_status():
    return {"server_status": "ok"}
