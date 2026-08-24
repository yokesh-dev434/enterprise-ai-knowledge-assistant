import os
import fitz
from docx import Document

from langchain_text_splitters import RecursiveCharacterTextSplitter
# class DocumentProcessor:

# extract a text
def extract_text(file_path):

    extension = os.path.splitext(file_path)[1].lower()
    # PDF
    if extension == ".pdf":

        doc = fitz.open(file_path)

        final_text = ""

        for page in doc:
            text = page.get_text()
            final_text += text + "\n"

        return final_text
    # DOCX
    elif extension == ".docx":

        doc = Document(file_path)

        final_text = ""

        for paragraph in doc.paragraphs:
            final_text += paragraph.text + "\n"

        return final_text

    # TXT
    elif extension == ".txt":

        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    else:
        raise ValueError(
            f"Unsupported file type: {extension}"
        )

# cleaning the text
def clean_text(raw_text_temp):
    tem_raw_text=""
    previous_empty=False
    for line in raw_text_temp.splitlines():
        if line =="":
            if previous_empty:# true
                continue
            else:
                tem_raw_text+="\n"
                previous_empty=True
        else:
            text = " ".join(line.split())
            tem_raw_text+=text+"\n"
            previous_empty=False
    return tem_raw_text.strip()

# chunking the cleaned text
# def chunk_text(cleaned_text,chunk_size,chunk_overlap):
#     chunks=[]
#     step =chunk_size-chunk_overlap
#     for i in range(0,len(cleaned_text),step):
#         chunk=cleaned_text[i:i+chunk_size]
#         # print(len(chunk))
#         # if chunk_size != len(chunk):
#         #     break
#         chunks.append(chunk)

#     return chunks




def chunk_text(cleaned_text,chunk_size=800,chunk_overlap=100):
    splitter =RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap
    )
    chunks = splitter.split_text(cleaned_text)
    return chunks