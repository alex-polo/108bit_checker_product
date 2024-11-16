from typing import Sequence

from sqlalchemy import select, RowMapping, Result

from src.database import get_async_session
from src.models import (
    Product,
    Manufacturer,
    ProductDescription,
    Category,
    product_to_category,
    product_to_category_108bit,
    Category108BIT,
    ProductImage,
    ProductDocument,
    ProductAttribute, EquipmentLines, Storage
)


async def get_products_for_categories(category_id: int):
    async for session in get_async_session():
        result = (await session.execute(
            select(Product)
            .select_from(Product, Category108BIT)
            .where(Product.categories_108bit)
            .where(Category108BIT.id == category_id)
        )).scalars().all()

        return result


async def get_products_for_categories_108bit():
    async for session in get_async_session():
        result = (await session.execute(
            select(Product.id)
            .select_from(Product, Category108BIT)
            .where(Product.categories_108bit)
        )).scalars().all()

        return result

async def get_desc_for_product(product_id: int):
    async for session in get_async_session():
        result = (await session.execute(
            select(ProductDescription.title, ProductDescription.description)
            .select_from(Product, ProductDescription)
            .where(Product.product_description)
            .where(Product.id == product_id)
        )).one_or_none()

        return result


async def get_manufacturer_for_product(product_id: int):
    async for session in get_async_session():
        result = (await session.execute(
            select(Manufacturer.name)
            .select_from(Product, Manufacturer)
            .where(Manufacturer.products)
            .where(Product.id == product_id)
        )).one_or_none()

        return result


async def get_images_for_product(product_id: int):
    async for session in get_async_session():
        result = (await session.execute(
            select(ProductImage.name, Storage.uuid)
            .join(Product, ProductImage.product_id == Product.id)
            .join(Storage, ProductImage.id == Storage.product_image_id)
            .where(Product.id == product_id)
        )).all()

        return result


async def get_documents_for_product(product_id: int):
    async for session in get_async_session():
        result = (await session.execute(
            select(ProductDocument.name, Storage.uuid)
            .join(Product, Product.id == ProductDocument.product_id)
            .join(Storage, ProductDocument.id == Storage.product_document_id)
            .where(Product.id == product_id)
        )).all()

        return result

async def get_attrs_for_product(product_id: int):
    async for session in get_async_session():
        result = (await session.execute(
            select(ProductAttribute.name, ProductAttribute.value)
            .join(Product, Product.id == ProductAttribute.product_id)
            .where(Product.id == product_id)
        )).all()

        return result

async def get_products(brand_name: str, category_id: int, exclude_108bit: bool) -> Sequence[RowMapping]:
    async for session in get_async_session():
        if exclude_108bit:
            query = (
                select(Product.id.label('product_id'),
                       Product.article.label('article'),
                       EquipmentLines.name.label('equipment_line'),
                       ProductDescription.title.label('title'),
                       ProductDescription.description.label('description'),
                       Category.id.label('category_id'),
                       Manufacturer.name.label('brand'))
                .join(Manufacturer, Product.manufacturer_id == Manufacturer.id)
                .outerjoin(EquipmentLines, Product.id == EquipmentLines.product_id)
                .join(ProductDescription, Product.id == ProductDescription.product_id)
                .join(product_to_category, Product.id == product_to_category.c.product_id)
                .join(Category, product_to_category.c.category_id == Category.id)
                .where(Manufacturer.name == brand_name)
                .where(Category.id == category_id)
            )
        else:
            query = (
                select(Product.id.label('product_id'),
                       Product.article.label('article'),
                       EquipmentLines.name.label('equipment_line'),
                       ProductDescription.title.label('title'),
                       ProductDescription.description.label('description'),
                       Category.id.label('category_id'),
                       Manufacturer.name.label('brand'))
                .join(Manufacturer, Product.manufacturer_id == Manufacturer.id)
                .outerjoin(EquipmentLines, Product.id == EquipmentLines.product_id)
                .join(ProductDescription, Product.id == ProductDescription.product_id)
                .join(product_to_category, Product.id == product_to_category.c.product_id)
                .join(Category, product_to_category.c.category_id == Category.id)
                .join(product_to_category_108bit, Product.id == product_to_category_108bit.c.product_id)
                .join(Category108BIT, product_to_category_108bit.c.category_id == Category108BIT.id)
                .where(Manufacturer.name == brand_name)
                .where(Category.id == category_id)
            )

        result: Result = await session.execute(query)
        rows_as_dict = result.mappings().all()
        return rows_as_dict

async def get_products_categories(brand_name: str) -> Sequence[int]:
    async for session in get_async_session():
        query = (
            select(Category.id)
            .join(product_to_category, Category.id == product_to_category.c.category_id)
            .join(Product, product_to_category.c.product_id == Product.id)
            .join(Manufacturer, Product.manufacturer_id == Manufacturer.id)
            .where(Manufacturer.name == brand_name)
        )

        categories_ids = (await session.execute(query)).scalars().all()
        return categories_ids


