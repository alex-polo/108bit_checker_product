import os.path
from typing import Optional
from uuid import UUID

from sqlalchemy import select

from src.database import get_async_session
from src.models import Storage, ProductDocument, ProductImage


async def get_path_document_file(filename: str) -> Optional[str]:
    async for session in get_async_session():
        query = (
            select(Storage.folder)
            .join(ProductDocument, Storage.product_document_id == ProductDocument.id)
            .where(ProductDocument.name == filename)
        )
        file_path = (await session.execute(query)).scalar()

        return None if file_path is None else os.path.join(file_path, filename)


async def get_path_document_file_by_uuid(uuid: UUID) -> Optional[tuple]:
    async for session in get_async_session():
        query_filename = (
            select(Storage.folder, Storage.filename)
            .join(ProductDocument, Storage.product_document_id == ProductDocument.id)
            .where(Storage.uuid == uuid)
        )
        result = (await session.execute(query_filename)).one_or_none()

        if result is not None:
            return result[1], os.path.join(*result)

        return None


async def get_path_image_file(filename: str) -> Optional[str]:
    async for session in get_async_session():
        query = (
            select(Storage.folder)
            .join(ProductImage, Storage.product_document_id == ProductImage.id)
            .where(ProductImage.name == filename)
        )
        file_path = (await session.execute(query)).scalar()

        return None if file_path is None else os.path.join(file_path, filename)


async def get_path_image_file_by_uuid(uuid: UUID) -> Optional[tuple]:
    async for session in get_async_session():
        query_filename = (
            select(Storage.folder, Storage.filename)
            .join(ProductImage, Storage.product_image_id == ProductImage.id)
            .where(Storage.uuid == uuid)
        )
        result = (await session.execute(query_filename)).one_or_none()

        if result is not None:
            return result[1], os.path.join(*result)

        return None
