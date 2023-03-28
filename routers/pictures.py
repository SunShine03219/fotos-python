from fastapi import APIRouter, UploadFile, File
from typing import Annotated

from logic.pictures_services import Pictures
from utils.middlewares.google_credentials_provider import (
    get_cloud_storage_client,
)
from utils.validators.pictures_services_validator import (
    file_or_folder_validator,
)

pic_router = APIRouter(prefix="/pictures", tags=["pictures"])

client = get_cloud_storage_client()


@pic_router.post("/files")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@pic_router.post("/upload")
async def upload_file(file: UploadFile):
    print("Entrei!")
    print(file.filename)
    return {"filename": "file.filename"}


@pic_router.get("/{file_path:path}")
async def read_file(file_path: str):
    is_folder = file_or_folder_validator(file_path)
    if is_folder:
        return await Pictures.get_files_path(file_path=file_path)

    else:
        return await Pictures.get_file_source(file_path=file_path)
