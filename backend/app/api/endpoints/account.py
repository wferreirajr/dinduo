from fastapi import APIRouter

router = APIRouter()

@router.get("/account")
def get_account():
    return {"message": "Hello World"}