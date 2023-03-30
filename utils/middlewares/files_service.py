import io
import os
import zipfile
from typing import List

from fastapi import UploadFile


async def extract_files(files: List[UploadFile]) -> List[UploadFile]:
    extracted_files = []
    for file in files:
        if file.filename.endswith(".zip"):
            zip_data = io.BytesIO(await file.read())
            with zipfile.ZipFile(zip_data) as myzip:
                folder_name = os.path.splitext(file.filename)[0]
                for zip_file in myzip.infolist():
                    file_data = myzip.read(zip_file.filename)
                    extracted_file = UploadFile(
                        file=io.BytesIO(file_data),
                        filename=f"{folder_name}/{zip_file.filename}",
                    )
                    extracted_files.append(extracted_file)
        else:
            extracted_files.append(file)
    return extracted_files
