import logging
from typing import Optional, List

from sqlalchemy import select

from . import categories_xml

from src.database import get_async_session
from src.models import Manufacturer

logger = logging.getLogger('server')


async def get_brand_id_by_name(brand_name: str) -> Optional[int]:
    async for session in get_async_session():
        query = select(Manufacturer.id).where(Manufacturer.name == brand_name)
        brand_id: int = (await session.execute(query)).scalar()

        return brand_id

async def get_products_for_brand_with_categories(brand_name: str, exclude_108bit: bool) -> List:
    xml_data = await categories_xml.create_xml(brand_name=brand_name, exclude_108bit=exclude_108bit)
    return xml_data