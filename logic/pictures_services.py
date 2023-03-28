import mimetypes
import os
from urllib.parse import quote

from fastapi import Response

from utils.exceptions.exception import InvalidCredentials
from utils.middlewares.google_credentials_provider import (
    get_cloud_storage_client,
)

client = get_cloud_storage_client()


class Pictures:
    def _create_tree(file_list: list):
        root = {}
        for path in file_list:
            current_node = root
            parts = path.split("/")
            for i, part in enumerate(parts):
                if not part:
                    continue
                if i == len(parts) - 1 and not part.endswith("/"):
                    current_node[part] = "File"
                else:
                    current_node = current_node.setdefault(part, {})
        if len(file_list) > 0:
            common_prefix = os.path.commonprefix(file_list)
            if common_prefix:
                prefix_parts = common_prefix.split("/")
                for part in prefix_parts[:-1]:
                    if part in root:
                        root = root[part]
        return root

    async def get_files_path(file_path: str = ""):
        if client:
            bucket = client.get_bucket("testes-roque")
            blob = bucket.blob(blob_name=file_path)

            blobs = bucket.list_blobs(prefix=blob.name)
            file_list = [quote(b.name) for b in blobs if b.name != blob.name]
            tree = Pictures._create_tree(file_list)
            return tree
        else:
            raise InvalidCredentials("Is there any empty credential")

    async def get_file_source(file_path: str):
        if client:
            bucket = client.get_bucket("testes-roque")
            blob = bucket.blob(blob_name=file_path)

            try:
                media_type, encoding = mimetypes.guess_type(blob.name)
                return Response(
                    content=blob.download_as_bytes(),
                    media_type="application/octet-stream",
                    headers={
                        "Content-Disposition": f"inline;"
                        f' filename="{blob.name}"',
                        "Content-Type": f"{media_type}",
                    },
                )
            except Exception as e:
                return {"Error": e}
        else:
            raise InvalidCredentials("Is there any empty credential")
