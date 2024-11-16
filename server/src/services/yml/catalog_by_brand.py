import logging
from typing import Sequence

from lxml import etree
from lxml.etree import Element
from sqlalchemy import select, Row, RowMapping

from src.database import get_async_session
from src.services.yml.elements import get_main_yml_element, set_attrs_product, set_images, set_documents
from src.models import (
    Product,
    Manufacturer,
    product_to_category_108bit,
    Category108BIT,
    ProductDescription,
    EquipmentLines
)

logger = logging.getLogger('server')


async def search_main_108bit_categories_by_brand(brand: str) -> Sequence[Row[tuple]]:
    query_id_main_categories = (
        select(Category108BIT.parent_id)
        .distinct()
        .select_from(Category108BIT)
        .join(product_to_category_108bit, Category108BIT.id == product_to_category_108bit.c.category_id)
        .join(Product, product_to_category_108bit.c.product_id == Product.id)
        .join(Manufacturer, Product.manufacturer_id == Manufacturer.id)
        .where(Manufacturer.name == brand)
    ).scalar_subquery()

    query_main_categories = (
        select(Category108BIT.id, Category108BIT.title)
        .distinct()
        .where(Category108BIT.id.in_(query_id_main_categories))
    )

    async for session in get_async_session():
        result = await session.execute(query_main_categories)

        return result.all()


async def get_child_108bit_categories(main_category_id: int) -> Sequence[Row[tuple]]:
    query = select(Category108BIT.id, Category108BIT.title).where(Category108BIT.parent_id == main_category_id)

    async for session in get_async_session():
        result = await session.execute(query)

        return result.all()


async def get_108_bit_products_by_brand(brand: str) -> Sequence[RowMapping]:
    query = (
        select(
            Category108BIT.id.label('category_id'),
            Product.id.label('product_id'),
            Product.quantity.label('quantity'),
            Product.price.label('price'),
            ProductDescription.title.label('title'),
            ProductDescription.description.label('description'),
            Manufacturer.name.label('manufacturer'),
            EquipmentLines.name.label('equipment_line')
               )
        .select_from(Product)
        .join(Manufacturer, Product.manufacturer_id == Manufacturer.id)
        .join(ProductDescription, Product.id == ProductDescription.product_id)
        .join(product_to_category_108bit, Product.id == product_to_category_108bit.c.product_id)
        .join(Category108BIT, Category108BIT.id == product_to_category_108bit.c.category_id)
        .outerjoin(EquipmentLines, EquipmentLines.product_id == Product.id)
        .where(Manufacturer.name == brand)
    )

    async for session in get_async_session():
        result = await session.execute(query)

        rows_as_dict = result.mappings().all()
        return rows_as_dict


async def set_offers(offers_element: etree.SubElement, brand: str):
    products_108bit = await get_108_bit_products_by_brand(brand=brand)
    count_products = len(products_108bit)
    logger.info(f'Query products: {count_products}')
    for product in products_108bit:

        offer_product = etree.SubElement(offers_element, "offer",
                                         id=str(product.get('product_id')), available="true")

        # etree.SubElement(offer_product, "url").text = product.url
        etree.SubElement(offer_product, "categoryId").text = str(product.get('category_id'))
        etree.SubElement(offer_product, "currencyId").text = "RUB"
        etree.SubElement(offer_product, "price").text = ('0'
                                                            if product.get('price') is None
                                                            else str(product.get('price')))
        etree.SubElement(offer_product, "quantity").text = ('0'
                                                            if product.get('quantity') is None
                                                            else str(product.get('quantity')))
        etree.SubElement(offer_product, "name").text =  product.get('title')
        etree.SubElement(offer_product, "description").text =  product.get('description')
        etree.SubElement(offer_product, "equipmentLine").text = product.get('equipment_line')
        etree.SubElement(offer_product, "manufacturer").text =  product.get('manufacturer')

        await set_attrs_product(product_id=product.get('product_id'), element=offer_product)
        await set_images(product_id=product.get('product_id'), element=offer_product)
        await set_documents(product_id=product.get('product_id'), element=offer_product)




async def set_categories(categories_element: Element, brand: str):
    main_categories = await search_main_108bit_categories_by_brand(brand=brand)

    for pk_key_category, title_main_category in main_categories:
        main_category_element = etree.SubElement(categories_element, "category", id=str(pk_key_category))
        main_category_element.text = title_main_category
        for pk_key_sub_cat, title_sub_cat in await get_child_108bit_categories(main_category_id=pk_key_category):
            etree.SubElement(categories_element, "category", id=str(pk_key_sub_cat), parentId=str(pk_key_category))


async def def_get_yml_catalog_by_brand(brand: str) -> str:
    root, shop = get_main_yml_element()

    # Добавляем категории
    categories = etree.SubElement(shop, "categories")
    await set_categories(categories_element=categories, brand=brand)

    # Добавляем продукты
    offers = etree.SubElement(shop, "offers")
    await set_offers(offers_element=offers, brand=brand)

    xml_data = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8')
    return xml_data