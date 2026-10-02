# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from docx2pdf import convert
# import fitz
# import os

# def extract_text(file_path):

#     extension = os.path.splitext(file_path)[1].lower()

#     # ---------------- PDF ----------------
#     if extension == ".pdf":

#         doc = fitz.open(file_path)

#         pages = []

#         for page_number, page in enumerate(doc, start=1):

#             text = page.get_text()

#             pages.append({
#                 "text": text,
#                 "page": page_number
#             })

#         doc.close()

#         return pages

#     # ---------------- DOCX ----------------
#     elif extension == ".docx":

#         # Create PDF path
#         pdf_path = os.path.splitext(file_path)[0] + ".pdf"

#         # Convert DOCX -> PDF
#         convert(file_path, pdf_path)

#         print(f"DOCX converted to PDF: {pdf_path}")

#         # Now extract PDF
#         doc = fitz.open(pdf_path)

#         pages = []

#         for page_number, page in enumerate(doc, start=1):

#             text = page.get_text()

#             pages.append({
#                 "text": text,
#                 "page": page_number
#             })

#         doc.close()

#         return pages

#     # ---------------- TXT ----------------
#     elif extension == ".txt":

#         with open(file_path, "r", encoding="utf-8") as file:

#             text = file.read()

#         return [{
#             "text": text,
#             "page": 1
#         }]

#     else:

#         raise ValueError(
#             f"Unsupported file type: {extension}"
#         )


# def clean_text(raw_text_temp):

#     if isinstance(raw_text_temp, list):

#         cleaned_pages = []

#         for page in raw_text_temp:

#             text = page["text"]

#             cleaned_text = ""
#             previous_empty = False

#             for line in text.splitlines():

#                 if line == "":
#                     if previous_empty:
#                         continue
#                     else:
#                         cleaned_text += "\n"
#                         previous_empty = True

#                 else:
#                     text_line = " ".join(line.split())
#                     cleaned_text += text_line + "\n"
#                     previous_empty = False

#             cleaned_pages.append({
#                 "text": cleaned_text.strip(),
#                 "page": page["page"]
#             })

#         return cleaned_pages

#     # DOCX / TXT
#     cleaned_text = ""
#     previous_empty = False

#     for line in raw_text_temp.splitlines():

#         if line == "":
#             if previous_empty:
#                 continue
#             else:
#                 cleaned_text += "\n"
#                 previous_empty = True

#         else:
#             text_line = " ".join(line.split())
#             cleaned_text += text_line + "\n"
#             previous_empty = False

#     return cleaned_text.strip()


# def chunk_text(cleaned_text, chunk_size=800, chunk_overlap=100):

#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=chunk_size,
#         chunk_overlap=chunk_overlap
#     )

#     # PDF
#     if isinstance(cleaned_text, list):

#         chunks = []

#         for page in cleaned_text:

#             page_chunks = splitter.split_text(page["text"])

#             for chunk in page_chunks:
#                 chunks.append({
#                     "text": chunk,
#                     "page": page["page"]
#                 })

#         return chunks

#     # DOCX / TXT
#     return [
#         {
#             "text": chunk,
#             "page": None
#         }
#         for chunk in splitter.split_text(cleaned_text)
#     ]



from langchain_text_splitters import RecursiveCharacterTextSplitter
from docx2pdf import convert
import fitz
import os


def extract_text(file_path):

    extension = os.path.splitext(file_path)[1].lower()

    # ---------------- PDF ----------------

    if extension == ".pdf":

        doc = fitz.open(file_path)

        pages = []

        for page_number, page in enumerate(doc, start=1):

            text = page.get_text()

            pages.append({
                "text": text,
                "page": page_number
            })

        doc.close()

        return pages

    # ---------------- DOCX ----------------

    elif extension == ".docx":

        # Convert DOCX to PDF
        pdf_path = os.path.splitext(file_path)[0] + ".pdf"

        convert(file_path, pdf_path)

        # Extract text from converted PDF
        doc = fitz.open(pdf_path)

        pages = []

        for page_number, page in enumerate(doc, start=1):

            text = page.get_text()

            pages.append({
                "text": text,
                "page": page_number
            })

        doc.close()

        return pages

    # ---------------- TXT ----------------

    elif extension == ".txt":

        with open(file_path, "r", encoding="utf-8") as file:

            text = file.read()

        return [{
            "text": text,
            "page": 1
        }]

    else:

        raise ValueError(
            f"Unsupported file type: {extension}"
        )


def clean_text(raw_text_temp):

    # PDF / DOCX converted to PDF
    if isinstance(raw_text_temp, list):

        cleaned_pages = []

        for page in raw_text_temp:

            text = page["text"]

            cleaned_text = ""
            previous_empty = False

            for line in text.splitlines():

                if line == "":

                    if previous_empty:
                        continue

                    cleaned_text += "\n"
                    previous_empty = True

                else:

                    text_line = " ".join(line.split())

                    cleaned_text += text_line + "\n"
                    previous_empty = False

            cleaned_pages.append({
                "text": cleaned_text.strip(),
                "page": page["page"]
            })

        return cleaned_pages

    # TXT
    cleaned_text = ""
    previous_empty = False

    for line in raw_text_temp.splitlines():

        if line == "":

            if previous_empty:
                continue

            cleaned_text += "\n"
            previous_empty = True

        else:

            text_line = " ".join(line.split())

            cleaned_text += text_line + "\n"
            previous_empty = False

    return cleaned_text.strip()


def chunk_text(
    cleaned_text,
    chunk_size=800,
    chunk_overlap=100
):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    # PDF / DOCX converted to PDF
    if isinstance(cleaned_text, list):

        chunks = []

        for page in cleaned_text:

            page_chunks = splitter.split_text(
                page["text"]
            )

            for chunk in page_chunks:

                chunks.append({
                    "text": chunk,
                    "page": page["page"]
                })

        return chunks

    # TXT fallback
    return [
        {
            "text": chunk,
            "page": None
        }
        for chunk in splitter.split_text(cleaned_text)
    ]