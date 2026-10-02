from datetime import datetime, timedelta, timezone

import jwt
from fastapi import APIRouter, HTTPException

from app.config.settings import settings
from app.schemas.login import login_Credtail_request


# JWT configuration
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"


# Simple user database for learning
simple_db_user_pass = {
    "UserName": "yokesh",
    "Password": "Hello@123"
}


login_router = APIRouter(
    prefix="/login",
    tags=["checking_login"]
)


@login_router.post("/LoginCredential")
def login(user_login: login_Credtail_request):

    # Check username
    if user_login.user_name != simple_db_user_pass.get("UserName"):
        raise HTTPException(
            status_code=401,
            detail="No username is found"
        )

    # Check password
    if user_login.password != simple_db_user_pass.get("Password"):
        raise HTTPException(
            status_code=401,
            detail="No password is matched"
        )

    # Create JWT payload
    payload = {
        "user_name": user_login.user_name,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }

    # Create access token
    access_token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "message": "user is matched",
        "access_token": access_token
    }