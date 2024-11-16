from typing import List

from lxml import etree
from sqlalchemy import select

from src.database import get_session
from src.models import InternetSite, Category, CategoryDescription
from src.services.db_query import get_products_for_categories_108bit, get_manufacturer_for_product

count_product = 0

def get_internet_sites():
    site_list = list()
    with get_session() as session:
        query = (select(InternetSite))
        return session.execute(query).scalars().all()


def get_main_category(site_id: int):
    site_list = list()
    with get_session() as session:
        query = (
            select(Category)
            .select_from(Category, InternetSite)
            .where(Category.internet_site)
            .where(InternetSite.id == site_id)
        )
        return session.execute(query).scalars().all()

def get_categories(category_id: int):
    with get_session() as session:
        query = (select(Category).where(Category.parent_id == category_id))
        return session.execute(query).scalars().all()

def category_description(category_id: int):
    with get_session() as session:
        return session.execute(
            select(CategoryDescription).where(CategoryDescription.category_id == category_id)
        ).scalar()



async def create_products(category_element, category_id: int, products_108bit: List[int]):
    global count_product

    with get_session() as session:
        for category in session.execute(select(Category).where(Category.id == category_id)).scalars():
            for product in category.products:
                # if product.id in products_108bit:
                #     continue

                manufacturer = (await get_manufacturer_for_product(product_id=product.id))[0]
                # if manufacturer != 'Esser by Honeywell':
                if manufacturer != 'Bosch':
                    continue
                else:
                    product_element = etree.SubElement(category_element, 'Product')
                    article = etree.SubElement(product_element, 'Article')
                    title = etree.SubElement(product_element, 'Title')
                    description = etree.SubElement(product_element, 'Description')
                    article.text = product.article
                    if product.product_description is None:
                        title.text = ''
                        description.text = ''
                    else:
                        description.text = product.product_description.description
                        title.text = product.product_description.title
                    count_product = count_product + 1





async def create_xml(products_108bit: List[int]):
    page = etree.Element('InternetSites')
    doc = etree.ElementTree(page)

    for site in get_internet_sites():
        internet_site = etree.SubElement(page, 'InternetSite', brand=site.name)

        for main_category in get_main_category(site.id):
            main_category_description = category_description(main_category.id)
            main_category_element = etree.SubElement(
                internet_site, 'Category',
                category_name=main_category_description.title,
            )
            await create_products(main_category_element, category_id=main_category.id, products_108bit=products_108bit)

            for sub_category in get_categories(category_id=main_category.id):
                sub_category_description = category_description(sub_category.id)

                sub_category_element = etree.SubElement(
                    main_category_element, 'Category',
                    category_name=sub_category_description.title,
                )
                await create_products(sub_category_element, category_id=sub_category.id, products_108bit=products_108bit)

                for sub_sub_category in get_categories(category_id=sub_category.id):
                    sub_sub_category_description = category_description(sub_sub_category.id)

                    sub_sub_category_element = etree.SubElement(
                        sub_category_element, 'Category',
                        category_name=sub_sub_category_description.title,
                    )
                    await create_products(sub_sub_category_element,
                                    category_id=sub_sub_category.id,
                                    products_108bit=products_108bit)

                    for sub_sub_sub_category in get_categories(category_id=sub_sub_category.id):
                        sub_sub_sub_category_description = category_description(sub_sub_sub_category.id)

                        sub_sub_sub_category_element = etree.SubElement(
                            sub_sub_category_element, 'Category',
                            category_name=sub_sub_sub_category_description.title,
                        )
                        await create_products(sub_sub_sub_category_element,
                                        category_id=sub_sub_sub_category.id,
                                        products_108bit=products_108bit)

    print(f'Count product: {count_product}')
    return doc

async def get_xml_catalog_exclude_108bit_with_category():
    # products_108bit_ids = await get_products_for_categories_108bit()
    products_108bit_ids = []

    xml_data = etree.tostring(await create_xml(products_108bit=products_108bit_ids),
                              pretty_print=True, xml_declaration=True, encoding='UTF-8')
    return xml_data