import logging
import os
import uuid

from fastapi import APIRouter, Response, HTTPException
from starlette.responses import FileResponse

from src.services.filesystem import (
    get_path_document_file,
    get_path_image_file, get_path_document_file_by_uuid
)

from src.services.yml import (
    get_yml_all_catalog,
    get_yml_categories,
    def_get_yml_catalog_by_brand
)
from src.tools import file_exist_exception

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
async def get_document(filename: str):
    file_path = await get_path_document_file(filename=filename)
    file_exist_exception(file_path=file_path)

    return FileResponse(file_path, filename=filename)


@store_router.get("/get-document-by-uuid")
async def get_image(document_uuid: str):
    try:
        uuid_obj = uuid.UUID(document_uuid, version=4)
        if str(uuid_obj) == document_uuid:
            file_query = await get_path_document_file_by_uuid(uuid=document_uuid)
            if file_query is not None:
                filename, file_path = file_query
                file_exist_exception(file_path=file_path)
                return FileResponse(file_path, filename=filename)
            else:
                raise HTTPException(status_code=404, detail="File not found")
    except ValueError:
        # Если возникает ошибка, строка не является валидным UUID
        raise HTTPException(status_code=404, detail='Invalid uuid data')




@store_router.get("/get-image-by-name")
async def get_image(filename: str):
    file_path = await get_path_image_file(filename=filename)
    file_exist_exception(file_path=file_path)

    return FileResponse(file_path, filename=filename)


# @store_router.get("/get-image-by-uuid")
# async def get_image(uuid: str):
#     file_path = await get_path_image_file(filename=filename)
#     file_exist_exception(file_path=file_path)
#
#     return FileResponse(file_path, filename=filename)

###########################   END FILESYSTEM    ###########################


# @store_router.get("/get-document/{file_name}")
# async def get_document(file_name: str):
#     file_path = await get_path_document_file(filename=file_name)
#
#     if file_path is None or not os.path.isfile(file_path):
#         raise HTTPException(status_code=404, detail="File not found")
#
#     return FileResponse(file_path, filename=file_name)
#
# @store_router.get("/get-image/{file_name}")
# async def get_image(file_name: str):
#     file_path = await get_path_image_file(filename=file_name)
#
#     if file_path is None or not os.path.isfile(file_path):
#         raise HTTPException(status_code=404, detail="File not found")
#
#     return FileResponse(file_path, filename=file_name)
