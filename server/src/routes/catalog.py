import logging

from fastapi import APIRouter, Response, Depends

from src.auth.manager import current_active_user
from src.models.user import User
from src.services.xml import get_products_for_brand_with_categories

logger = logging.getLogger('server')

catalog_router = APIRouter(
    prefix='/catalog',
    tags=["catalog"],
)


@catalog_router.get("/products", response_class=Response, responses={
        200: {
            "content": {"application/xml": {}},
            "description": "Successful response YML data in XML format",
        }})
async def products(brand: str, exclude_108bit: bool = True,
                   # user: User = Depends(current_active_user)
                   ):
    xml_data = await get_products_for_brand_with_categories(brand_name=brand, exclude_108bit=exclude_108bit)
    return Response(content=xml_data, media_type="application/xml")