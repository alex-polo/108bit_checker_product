import logging
import mimetypes
import time
import uuid

from starlette.responses import FileResponse
from fastapi import (
    APIRouter,
    Response,
    HTTPException,
    Path,
    Depends
)

from src.auth.manager import current_active_user
from src.models import User
from src.services.filesystem import (
    get_path_document_file,
    get_path_image_file,
    get_path_document_file_by_uuid,
    get_path_image_file_by_uuid
)

from src.services.yml import (
    get_yml_all_catalog,
    get_yml_categories,
    def_get_yml_catalog_by_brand
)

from src.tools import is_file_exist

logger = logging.getLogger('server')

filename_regex = r'^[\w,\s-]+\.[A-Za-z]{3}$'

store_router = APIRouter(
    prefix='/store',
    tags=["108bit"],
)


#############################   CATALOG'S    #############################

@store_router.get(path="/get-catalog",
                  summary='Возвращает весь каталог в формате XML',
                  response_class=Response,
                  responses={
                      200: {
                          "content": {"application/xml": {}},
                          "description": "Successful response YML data in XML format",
                      },
                      401: {"description": "Unauthorized - Требуется авторизация"},
                  }
                  )
async def get_all_catalog(user: User = Depends(current_active_user)):
    """
                       Возможные ответы:
                       - **200**: Возвращает весь каталог в формате XML.
                       - **401**: Требуется авторизация.
    """
    logger.info(f'Start method "get_all_catalog"')
    start_time = time.time()
    yml_data = await get_yml_all_catalog()

    logger.info(f'Method "get_all_catalog" Execution time: {round(time.time() - start_time, 3)}')
    return Response(content=yml_data, media_type="application/xml")


@store_router.get(path='/get-catalog-by-brand',
                  summary='Возвращает каталог в формате XML по названию производителя (Чувствителен к регистру)',
                  response_class=Response,
                  responses={
                      200: {
                          "content": {"application/xml": {}},
                          "description": "Successful response YML data in XML format",
                      },
                      401: {"description": "Unauthorized - Требуется авторизация"},
                  }
                  )
async def get_yml_catalog_by_brand(brand: str, user: User = Depends(current_active_user)):
    """
                   Возвращает каталог по названию производителя (Чувствителен к регистру).

                   - **brand**: Название производителя.

                   Возможные ответы:
                   - **200**: Возвращает каталог в формате XML.
                   - **401**: Требуется авторизация.
    """
    logger.info(f'Start method "get_yml_catalog_by_brand"')
    start_time = time.time()
    yml_data = await def_get_yml_catalog_by_brand(brand=brand)
    logger.info(f'Method "get_yml_catalog_by_brand" Execution time: {round(time.time() - start_time, 3)}')
    return Response(content=yml_data, media_type="application/xml")


@store_router.get(path="/get-categories",
                  summary='Возвращает все категории',
                  response_class=Response,
                  responses={
                      200: {
                          "content": {"application/xml": {}},
                          "description": "Successful response YML data in XML format",
                      },
                      401: {"description": "Unauthorized - Требуется авторизация"},
                  })
async def get_categories(user: User = Depends(current_active_user)):
    """
                           Возможные ответы:
                           - **200**: Возвращает категории в формате XML.
                           - **401**: Требуется авторизация.
    """
    logger.info(f'Start method "get_categories"')
    start_time = time.time()
    yml_data = await get_yml_categories()
    logger.info(f'Method "get_categories" Execution time: {round(time.time() - start_time, 3)}')
    return Response(content=yml_data, media_type="application/xml")


###########################   END CATALOG'S    ############################
#############################   FILESYSTEM    #############################

@store_router.get(path="/get-document-by-name",
                  summary='Получить документ по имени файла (Чувствителен к регистру)',
                  responses={
                      200: {
                          "content": {
                              "application/pdf": {},
                          },
                          "description": "Успешное получение документа",
                      },
                      401: {"description": "Unauthorized - Требуется авторизация"},
                      404: {
                          "description": "Файл не найден",
                          "content": {
                              "application/json": {
                                  "details": {"detail": "File not found"}
                              }
                          }
                      },
                      422: {
                          "description": "Unprocessable Entity. Ошибка валидации имени файла",
                          "content": {
                              "application/json": {
                                  "details": {"detail": "Filename not valid"}
                              }
                          }
                      }
                  }
                  )
async def get_document_by_name(filename: str = Path(..., regex=filename_regex),
                               user: User = Depends(current_active_user)):
    """
               Возвращает документ по имени файла.

               - **filename**: Имя файла документа (Чувствителен к регистру).

               Возможные ответы:
               - **200**: Возвращает файл документа.
               - **401**: Требуется авторизация.
               - **404**: Файл не найден или передано некорректное имя.
               - **422**: Unprocessable Entity. Ошибка валидации Filename.
       """
    logger.info(f'Start method "get-document-by-name", document_filename: {filename}')
    start_time = time.time()
    file_path = await get_path_document_file(filename=filename)

    if file_path is not None:
        if is_file_exist(file_path=file_path):
            logger.info(f'Method "get_document_by_name" Execution time: {round(time.time() - start_time, 3)}')
            return FileResponse(path=file_path, media_type='application/pdf', filename=filename)

    logger.info(f'Method "get_document_by_name" Execution time: {round(time.time() - start_time, 3)}')
    raise HTTPException(status_code=404, detail="File not found")


@store_router.get(path="/get-document-by-uuid",
                  summary='Получить документ по UUID',
                  responses={
                      200: {
                          "content": {
                              "application/pdf": {},
                          },
                          "description": "Успешное получение документа",
                      },
                      401: {"description": "Unauthorized - Требуется авторизация"},
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
async def get_document_by_uuid(document_uuid: uuid.UUID, user: User = Depends(current_active_user)):
    """
            Возвращает документ по UUID.

            - **document_uuid**: UUID файла документа.

            Возможные ответы:
            - **200**: Возвращает файл документа.
            - **401**: Требуется авторизация.
            - **404**: Файл не найден или передан некорректный UUID.
            - **422**: Unprocessable Entity. Ошибка валидации UUID.
    """
    logger.info(f'Start method "get_document_by_uuid", image_uuid: {document_uuid}')
    start_time = time.time()
    file_query = await get_path_document_file_by_uuid(uuid=document_uuid)

    if file_query is not None:
        filename, file_path = file_query
        if is_file_exist(file_path=file_path):
            logger.info(f'Method "get_document_by_uuid" Execution time: {round(time.time() - start_time, 3)}')
            return FileResponse(path=file_path, media_type="application/pdf", filename=filename)

    logger.info(f'Method "get_document_by_uuid" Execution time: {round(time.time() - start_time, 3)}')
    raise HTTPException(status_code=404, detail="File not found")


@store_router.get(path="/get-image-by-name",
                  summary='Получить изображение по имени файла (Чувствителен к регистру)',
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
                      401: {"description": "Unauthorized - Требуется авторизация"},
                      404: {
                          "description": "Файл не найден",
                          "content": {
                              "application/json": {
                                  "details": {"detail": "File not found"}
                              }
                          }
                      },
                      422: {
                          "description": "Unprocessable Entity. Ошибка валидации имени файла",
                          "content": {
                              "application/json": {
                                  "details": {"detail": "Filename not valid"}
                              }
                          }
                      }
                  }
                  )
async def get_image_by_name(filename: str = Path(..., regex=filename_regex),
                            user: User = Depends(current_active_user)):
    """
            Возвращает изображение по имени файла.

            - **filename**: Имя файла изображения (Чувствителен к регистру).

            Возможные ответы:
            - **200**: Возвращает файл изображения.
            - **401**: Требуется авторизация.
            - **404**: Файл не найден или передано некорректное имя.
            - **422**: Unprocessable Entity. Ошибка валидации Filename.
    """
    logger.info(f'Start method "get_image_by_name", image_filename: {filename}')
    start_time = time.time()
    file_path = await get_path_image_file(filename=filename)

    if file_path is not None:
        if is_file_exist(file_path=file_path):
            mime_type, _ = mimetypes.guess_type(file_path)
            logger.info(f'Method "get_image_by_name" Execution time: {round(time.time() - start_time, 3)}')
            return FileResponse(path=file_path, media_type=mime_type, filename=filename)

    logger.info(f'Method "get_image_by_name" Execution time: {round(time.time() - start_time, 3)}')
    raise HTTPException(status_code=404, detail="File not found")


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
        401: {"description": "Unauthorized - Требуется авторизация"},
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
async def get_image_by_uuid(image_uuid: uuid.UUID, user: User = Depends(current_active_user)):
    """
            Возвращает изображение по UUID.

            - **image_uuid**: UUID файла изображения.

            Возможные ответы:
            - **200**: Возвращает файл изображения.
            - **401**: Требуется авторизация.
            - **404**: Файл не найден или передан некорректный UUID.
            - **422**: Unprocessable Entity. Ошибка валидации UUID.
    """
    logger.info(f'Start method "get_image_by_uuid", image_uuid: {image_uuid}')
    start_time = time.time()
    file_query = await get_path_image_file_by_uuid(uuid=image_uuid)

    if file_query is not None:
        filename, file_path = file_query
        if is_file_exist(file_path=file_path):
            mime_type, _ = mimetypes.guess_type(file_path)
            logger.info(f'Method "get_image_by_uuid" Execution time: {round(time.time() - start_time, 3)}')
            return FileResponse(path=file_path, media_type=mime_type, filename=filename)

    logger.info(f'Method "get_image_by_uuid" Execution time: {round(time.time() - start_time, 3)}')
    raise HTTPException(status_code=404, detail="File not found")

###########################   END FILESYSTEM    ###########################
