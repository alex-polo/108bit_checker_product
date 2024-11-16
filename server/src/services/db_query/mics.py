from typing import Sequence, List

from sqlalchemy import select

from src.database import get_async_session
from src.models import Category, InternetSite


async def get_all_categories_ids() -> Sequence[int]:
    async for session in get_async_session():
        categories_ids = (
            await session.execute(select(Category.id).where(Category.parent_id.is_(None)))).scalars().all()
        return categories_ids


async def get_internet_sites(category_ids: List[int]) -> List[dict]:
    async for session in get_async_session():
        internet_sites = (await session.execute(
            select(InternetSite.name, Category.id)
            .join(Category, Category.internet_site_id == InternetSite.id)
            .where(Category.id.in_(category_ids))
        )).fetchall()

        site_names = set([site for site, _ in internet_sites])
        internet_sites_as_dict = list()

        for site_name in site_names:
            categories_id_list = list()
            for internet_site, category_id in internet_sites:
                if site_name == internet_site:
                    categories_id_list.append(category_id)
            internet_sites_as_dict.append(
                {
                    'internet_site': site_name,
                    'categories_ids': categories_id_list
                }
            )

        return internet_sites_as_dict