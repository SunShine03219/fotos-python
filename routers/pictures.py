from typing import List

from fastapi import APIRouter, UploadFile

from logic.pictures_services import Pictures
from utils.exceptions.exception import InvalidPathOrFile
from utils.middlewares.files_service import extract_files
from utils.validators.pictures_services_validator import (
    file_or_folder_validator,
)

pic_router = APIRouter(prefix="/pictures", tags=["pictures"])


@pic_router.post("/upload/{file_path:path}")
async def upload_file(file_path: str, file: List[UploadFile]):
    is_folder = file_or_folder_validator(file_path)
    if is_folder:
        files_to_upload = await extract_files(file)
        return await Pictures.upload_files(files_to_upload, file_path)

    raise InvalidPathOrFile("There were problems with the order")


@pic_router.post("/folder/create/{file_path:path}")
async def create_folder(file_path: str):
    return await Pictures.create_folder(file_path)


@pic_router.delete("/delete/{file_path:path}")
async def delete_file(file_path: str):
    is_folder = file_or_folder_validator(file_path)
    if is_folder:
        return await Pictures.delete_folder(file_path)
    else:
        return await Pictures.delete_file(file_path)


@pic_router.get("/download/{file_path:path}")
async def download_file(file_path: str):
    is_folder = file_or_folder_validator(file_path)
    if is_folder:
        return await Pictures.download_folder(file_path)
    else:
        return await Pictures.download_file(file_path)


@pic_router.get("/{file_path:path}")
async def read_file(file_path: str):
    is_folder = file_or_folder_validator(file_path)
    if is_folder:
        return await Pictures.get_files_path(file_path=file_path)

    else:
        return await Pictures.get_file_source(file_path=file_path)
