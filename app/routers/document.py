from fastapi import APIRouter,HTTPException,UploadFile,File,Form,Depends
from enum import Enum
import uuid


from app.services.document_service import save_document
from app.services.document_processor import extract_text
from app.ingestion.ingest_document import ingest_document
from app.services.auth_service import get_current_user

document_router = APIRouter(prefix="/documents",tags=["document"])





class Department(str, Enum):
    HR = "HR"
    IT = "IT"
    FINANCE = "Finance"
    ENGINEERING = "Engineering"
    CLIENT = "Client"
    PRODUCT = "PROJECTS"




def mb_to_bytes(mb_size):
    # Multiplies the MB value by 1,024 twice to get bytes
    return mb_size * 1024 * 1024

@document_router.post("/")
async def upload_file(file: UploadFile = File(...), department: Department = Form(...), current_user: dict = Depends(get_current_user)):
    if file.filename.lower().endswith((".pdf",".txt",".docx")) :# bytes 10 mb
        if file.size <= mb_to_bytes(10):
            document_id = str(uuid.uuid4())

            destination_path =await save_document(file, department)

            pdf_text = extract_text(str(destination_path))

            metadata = {
                "document_id": document_id,
                "department": department.value.title(),
                "source": file.filename,
                "file_type": file.filename.split(".")[-1].lower()
            }
            ingest_document(
                str(destination_path),
                metadata
            )
            return {
                "document_id":document_id ,
                "message":"Uploaded Successfully",
                "filename": file.filename,
                "file_text":pdf_text,
                "metadata" : metadata
            }
        else:
            raise HTTPException(
                status_code =400,
                detail = "File size must not exceed 10 MB."
            )

    else:
        raise HTTPException(
            status_code=400,
            detail = "Only PDF, DOCX and TXT files are allowed."
        )


    


"""

# class DocumentResponse(BaseModel):
#     mesage :str
#     filename :str

{
  "filename": "Enterprise_AI_Knowledge_Assistant_Sample_Policy.pdf",
  "file": {
    "_file": {},
    "_max_size": 1048576,
    "_rolled": false,
    "_TemporaryFileArgs": {
      "mode": "w+b",
      "buffering": -1,
      "suffix": null,
      "prefix": null,
      "encoding": null,
      "newline": null,
      "dir": null,
      "errors": null
    }
  },
  "size": 23314,
  "headers": {
    "content-disposition": "form-data; name=\"file\"; filename=\"Enterprise_AI_Knowledge_Assistant_Sample_Policy.pdf\"",
    "content-type": "application/pdf"
  },
  "_max_mem_size": 1048576
}
"""