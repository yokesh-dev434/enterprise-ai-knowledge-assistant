
from pathlib import Path

async def save_document(file, department):
    department_folder = Path("data/documents") / department.value

    department_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    file_path = department_folder / file.filename

    content = await file.read()

    with open(file_path, "wb") as newfile:
        newfile.write(content)

    return file_path