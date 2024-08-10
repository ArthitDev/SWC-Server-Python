from fastapi import APIRouter, Response, status

router = APIRouter()


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(response: Response):
    response.delete_cookie(key="accessToken", path="/")
    response.delete_cookie(key="refreshToken", path="/")
    return {"message": "Logged out successfully"}
