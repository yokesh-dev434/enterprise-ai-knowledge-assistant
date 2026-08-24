
from fastapi import FastAPI,HTTPException
from fastapi import BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.config.settings import settings

# print(settings.APP_NAME)
from fastapi.responses import JSONResponse
from app.exceptions.document import DocumentNotFoundError


from app.routers.employee import router
from app.routers.document import document_router
from app.routers.auth import auth_router




def process_document(filename):
    for i in range(10000):
        print(i)
    print(f"Processing {filename}")



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

app.include_router(router)
app.include_router(document_router)
app.include_router(auth_router)

@app.get("/test-error")
def test_error():
    raise DocumentNotFoundError()

@app.post("/background-test")
async def background_test(background_tasks: BackgroundTasks):

    background_tasks.add_task(
        process_document,
        "sample.pdf"
    )

    return {
        "message": "Task added"
    }