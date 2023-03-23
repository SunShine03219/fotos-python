import mimetypes

from fastapi import Response

from utils.middlewares.google_credentials_provider import (
    get_cloud_storage_client,
)

client = get_cloud_storage_client()


class Pictures:
    async def get_files_path(file_path: str = ""):
        bucket = client.get_bucket("testes-roque")
        blob = bucket.blob(blob_name=file_path)

        blobs = bucket.list_blobs(prefix=blob.name)
        file_list = [b.name for b in blobs if b.name != blob.name]
        return file_list

    async def get_image(file_path: str):
        bucket = client.get_bucket("testes-roque")
        blob = bucket.blob(blob_name=file_path)
        try:
            media_type, encoding = mimetypes.guess_type(blob.name)
            return Response(
                content=blob.download_as_bytes(),
                media_type="application/octet-stream",
                headers={
                    "Content-Disposition": f'inline; filename="{blob.name}"',
                    "Content-Type": f"{media_type}",
                },
            )
        except Exception as e:
            return {"Error": e}
