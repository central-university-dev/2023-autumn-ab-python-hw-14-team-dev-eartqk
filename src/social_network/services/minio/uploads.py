import json
from uuid import uuid4

from fastapi import File, HTTPException, UploadFile, status
from minio import Minio
from minio.error import S3Error

from src.social_network.settings import settings

from .policies import media_download_policy


class UploadsService:
    def __init__(self):
        self.client = Minio(
            settings.minio_host,
            access_key=settings.minio_user,
            secret_key=settings.minio_password,
            secure=False,
        )

        if not self.client.bucket_exists('media'):
            self.client.make_bucket('media')
            self.client.set_bucket_policy('media', json.dumps(media_download_policy))

    def _upload(self, file: UploadFile = File(...)) -> str:
        try:
            file_ext = file.filename.split('.')[-1]  # type: ignore
            new_filename = uuid4().hex + '.' + file_ext
        except AttributeError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Failed to upload file.'
            ) from e

        try:
            response = self.client.put_object(
                bucket_name='media',
                object_name=new_filename,
                data=file.file,
                length=file.size,
                content_type=file.content_type,
                metadata={'x-amz-meta-public': 'true'},
            )

            return str(response.object_name)
        except S3Error as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Failed to upload file.'
            ) from e

    def upload_file(self, file: UploadFile = File(...), only_picture: bool = False) -> str:
        if file.filename:
            file_ext = file.filename.split('.')[-1]
        else:
            file_ext = None

        if only_picture and file_ext not in ['jpg', 'jpeg', 'png']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='File type not allowed.')
        if file_ext not in ['jpg', 'jpeg', 'png', 'mp4']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='File type not allowed.')

        return self._upload(file)

    def upload_files(self, files: list[UploadFile] = File(...)) -> list[str]:
        filenames = []
        for file in files:
            name = self._upload(file)
            filenames.append(name)
        return filenames
