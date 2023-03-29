from typing import List

from fastapi import APIRouter, UploadFile

from logic.pictures_services import Pictures
from utils.exceptions.exception import InvalidPathOrFile
from utils.middlewares.files_service import extract_files
from utils.middlewares.google_credentials_provider import (
    get_cloud_storage_client,
)
from utils.validators.pictures_services_validator import (
    file_or_folder_validator,
)

pic_router = APIRouter(prefix="/pictures", tags=["pictures"])

client = get_cloud_storage_client()


@pic_router.post("/upload/{file_path:path}")
async def upload_file(file_path: str, file: List[UploadFile]):
    is_folder = file_or_folder_validator(file_path)
    if is_folder:
        files_to_upload = await extract_files(file)
        return await Pictures.upload_files(files_to_upload, file_path)

    raise InvalidPathOrFile("There were problems with the order")


@pic_router.get("/{file_path:path}")
async def read_file(file_path: str):
    is_folder = file_or_folder_validator(file_path)
    if is_folder:
        return await Pictures.get_files_path(file_path=file_path)

    else:
        return await Pictures.get_file_source(file_path=file_path)
