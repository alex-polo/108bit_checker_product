from typing import Sequence

from sqlalchemy import select, Result

from src.database import get_async_session
from src.models import Category, CategoryDescription, Category108BIT


async def get_108bit_main_categories():
    async for session in get_async_session():
        result = (await session.execute(
            select(Category108BIT.id, Category108BIT.title).where(Category108BIT.parent_id == None)
        )).all()

        return result

async def get_108bit_sub_categories(category_id: int):
    async for session in get_async_session():
        result = (await session.execute(
            select(Category108BIT.id, Category108BIT.title).where(Category108BIT.parent_id == category_id)
        )).all()

        return result


async def get_all_id_108bit_categories():
    async for session in get_async_session():
        return (await session.execute(select(Category108BIT.id))).scalars().all()



async def get_parent_category(category_id: int):
    async for session in get_async_session():
        current_category_id = category_id
        while True:
            category_id = (
                await session.execute(select(Category.parent_id).where(Category.id == current_category_id)
                                      )).scalar()

            if category_id is None:
                break

            current_category_id = category_id

        return current_category_id


async def get_child_category(category_id: int):
    async for session in get_async_session():
        query = (
            select(Category.id.label('category_id'), CategoryDescription.title.label('title'))
            .join(CategoryDescription, Category.id == CategoryDescription.category_id)
            .where(Category.parent_id == category_id)
        )

        result: Result = await session.execute(query)
        rows_as_dict = result.mappings().all()
        return rows_as_dict


async def get_title_category(category_id: int):
    async for session in get_async_session():
        query = (
            select(CategoryDescription.title)
            .join(Category, Category.id == CategoryDescription.category_id)
            .where(Category.id == category_id)
        )

        result: Result = await session.execute(query)
        return result.scalar()


async def get_parents_category(category_ids: Sequence[int]):
    async for session in get_async_session():
        current_category_ids = category_ids
        main_category_ids = set()
        while len(current_category_ids) > 0:
            category_ids = (await session.execute(select(Category.id, Category.parent_id)
                                      .where(Category.id.in_(current_category_ids))
                                      )).all()

            current_category_ids = list()
            for category_id, parent_id in category_ids:
                if parent_id is not None:
                    current_category_ids.append(parent_id)
                else:
                    main_category_ids.add(category_id)

        return list(main_category_ids)