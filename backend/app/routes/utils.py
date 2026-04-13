from fastapi import APIRouter

router = APIRouter(prefix="/utils")


@router.get("/health")
def health_check():
    # add neon db check
    return True
