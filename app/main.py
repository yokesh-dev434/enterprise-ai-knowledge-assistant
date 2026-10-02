
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.exceptions.document import DocumentNotFoundError
#
from app.routers.document import document_router
from app.routers.chat import chat_app
from app.routers.login import login_router








app = FastAPI()

@app.exception_handler(DocumentNotFoundError)
async def document_not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Document not found"
        }
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins =["*"],
    allow_credentials =True,
    allow_methods =["*"],
    allow_headers =["*"]

)

@app.middleware("http")
async def log_request(request,call_next):
    print("Request received")
    response = await call_next(request)
    print("response completed")
    return response

# app.include_router(router)
app.include_router(document_router)

app.include_router(chat_app)
app.include_router(login_router)

# @app.get("/test-error")
# def test_error():
#     raise DocumentNotFoundError()
