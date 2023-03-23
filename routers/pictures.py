from fastapi import APIRouter

from logic.pictures_services import Pictures
from utils.middlewares.google_credentials_provider import (
    get_cloud_storage_client,
)
from utils.validators.pictures_services_validator import (
    file_or_folder_validator,
)

pic_router = APIRouter(prefix="/pictures", tags=["pictures"])

client = get_cloud_storage_client()


@pic_router.get("/list")
async def list_files():
    bucket = client.get_bucket("testes-roque")
    blobs = bucket.list_blobs()
    file_list = [blob.name for blob in blobs]
    print(blobs.__dict__)
    return file_list


@pic_router.get("/{file_path:path}")
async def read_file(file_path: str):
    is_folder = file_or_folder_validator(file_path)
    if is_folder:
        return await Pictures.get_files_path(file_path=file_path)

    else:
        return await Pictures.get_image(file_path=file_path)
