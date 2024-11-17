import logging
import mimetypes
import uuid

from fastapi import APIRouter, Response, HTTPException
from starlette.responses import FileResponse

from src.services.filesystem import (
    get_path_document_file,
    get_path_image_file, get_path_document_file_by_uuid, get_path_image_file_by_uuid
)

from src.services.yml import (
    get_yml_all_catalog,
    get_yml_categories,
    def_get_yml_catalog_by_brand
)
from src.tools import is_file_exist

logger = logging.getLogger('server')

store_router = APIRouter(
    prefix='/store',
    tags=["108bit"],
)


# if user.is_news_bot is False:
#     raise HTTPException(fastapi.status.HTTP_403_FORBIDDEN, 'User does not have permissions')


#############################   CATALOG'S    #############################

@store_router.get("/get-catalog",
                  response_class=Response,
                  responses={
                      200: {
                          "content": {"application/xml": {}},
                          "description": "Successful response YML data in XML format",
                      }
                  }
                  )
async def get_catalog():
    yml_data = await get_yml_all_catalog()
    return Response(content=yml_data, media_type="application/xml")


@store_router.get("/get-categories", response_class=Response, responses={
    200: {
        "content": {"application/xml": {}},
        "description": "Successful response YML data in XML format",
    }})
async def get_categories():
    yml_data = await get_yml_categories()
    return Response(content=yml_data, media_type="application/xml")


@store_router.get('/get-catalog-by-brand')
async def get_yml_catalog_by_brand(brand: str):
    yml_data = await def_get_yml_catalog_by_brand(brand=brand)
    return Response(content=yml_data, media_type="application/xml")


###########################   END CATALOG'S    ############################
#############################   FILESYSTEM    #############################

@store_router.get("/get-document-by-name")
async def get_document_by_name(filename: str):
    file_path = await get_path_document_file(filename=filename)
    is_file_exist(file_path=file_path)

    return FileResponse(file_path, filename=filename)


@store_router.get("/get-document-by-uuid/{document_uuid}",
                  summary="Получить документ по UUID",
                  # description=,
                  responses={
                      200: {
                          'media_type': "application/pdf",
                          "description": "Успешное получение изображения",
                      },
                      404: {
                          "description": "Файл не найден или UUID недействителен",
                          "content": {
                              "application/json": {
                                  "example": {"detail": "File not found"}
                              }
                          }
                      }
                  },
                  )
async def get_document_by_uuid(document_uuid: str):
    """
        Возвращает изображение по UUID.

        - **document_uuid**: UUID файла изображения.

        Возможные ответы:
        - **200**: Возвращает файл изображения.
        - **404**: Если файл не найден или передан некорректный UUID.
        """
    try:
        uuid_obj = uuid.UUID(document_uuid, version=4)
        if str(uuid_obj) == document_uuid:
            file_query = await get_path_document_file_by_uuid(uuid=document_uuid)
            if file_query is not None:
                filename, file_path = file_query
                is_file_exist(file_path=file_path)
                return FileResponse(path=file_path, media_type="application/pdf", filename=filename)
            else:
                raise HTTPException(status_code=404, detail="File not found")
    except ValueError:
        # Если возникает ошибка, строка не является валидным UUID
        raise HTTPException(status_code=404, detail='Invalid uuid data')


@store_router.get("/get-image-by-name")
async def get_image_by_name(filename: str):
    file_path = await get_path_image_file(filename=filename)
    is_file_exist(file_path=file_path)

    return FileResponse(file_path, filename=filename)


@store_router.get(
    path="/get-image-by-uuid",
    summary='Получить изображение по UUID',
    responses={
        200: {
            "content": {
                "image/png": {},
                "image/jpeg": {},
                "image/gif": {},
                "image/webp": {},
                "image/svg+xml": {}
            },
            "description": "Успешное получение изображения",
        },
        404: {
            "description": "Файл не найден или UUID недействителен",
            "content": {
                "application/json": {
                    "details": {"detail": "File not found"}
                }
            }
        },
        422: {
            "description": "Unprocessable Entity. Ошибка валидации UUID",
            "content": {
                "application/json": {
                    "details": {"detail": "UUID not valid"}
                }
            }
        }
    }
)
async def get_image_by_uuid(image_uuid: uuid.UUID):
    """
            Возвращает изображение по UUID.

            - **image_uuid**: UUID файла изображения.

            Возможные ответы:
            - **200**: Возвращает файл изображения.
            - **404**: Файл не найден или передан некорректный UUID.
            - **422**: Unprocessable Entity. Ошибка валидации UUID.
    """
    logger.info(f'Start method get_image_by_uuid, image_uuid: {image_uuid}')
    file_query = await get_path_image_file_by_uuid(uuid=image_uuid)
    print(file_query)
    if file_query is not None:
        filename, file_path = file_query
        if is_file_exist(file_path=file_path):
            mime_type, _ = mimetypes.guess_type(file_path)
            return FileResponse(path=file_path, media_type=mime_type, filename=filename)

    raise HTTPException(status_code=404, detail="File not found")

###########################   END FILESYSTEM    ###########################
