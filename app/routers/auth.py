# from fastapi import APIRouter,HTTPException
# from app.schemas.auth import LoginBase

# import jwt
# from datetime import datetime,timezone,timedelta


# from fastapi import APIRouter,HTTPException
# router = APIRouter(prefix="/documents",tags=["login"])

# auth_router =APIRouter(prefix="/auth",tags=["login"])
# SECRET_KEY="fhdsjhfiuyuerujg"
# ALGORITHM ="HS256"

# resister_account={
#     "yoki":"Yokesh@2612"
# }


# @auth_router.post("/login")
# def LoginRequest(login_info:LoginBase):
#     if login_info.username in resister_account:
#         password =resister_account[login_info.username]
#         if password == login_info.password:
#             payload= {
#                 "user_id":1234,
#                 "username":login_info.username,
#                 "exp":datetime.now(timezone.utc) + timedelta(minutes=10),
#                 "iat":datetime.now(timezone.utc)
#             }
#             token = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)

#             return {
#                 "JWT":token,
#                 "message": "login Successfully"
#             }
#         else:
#             raise HTTPException(
#                         status_code=401,
#                         detail="Wrong password"
#                     )
#     else:
#         raise HTTPException(
#             status_code=401,
#             detail="unauthorized"
#         )



