import logging
from typing import List, Sequence

from lxml import etree
from sqlalchemy import RowMapping

from src.services.db_query import (
    get_products_categories,
    get_parents_category,
    get_internet_sites,
    get_title_category,
    get_products,
    get_child_category
)

logger = logging.getLogger('server')


async def search_main_data(brand_name: str) -> List[dict]:
    products_categories_ids = await get_products_categories(brand_name=brand_name)
    main_categories = await get_parents_category(category_ids=products_categories_ids)
    internet_sites_collection = await get_internet_sites(category_ids=main_categories)
    return internet_sites_collection


async def create_products_elements(products: Sequence[RowMapping], category_element: etree.Element):
    for data_product in products:
        manufacturer = data_product.get('brand')
        article = data_product.get('article')
        title = data_product.get('title')
        description = data_product.get('description')
        equipment_line = data_product.get('equipment_line')

        product_element = etree.SubElement(category_element, 'Product')
        article_element = etree.SubElement(product_element, 'Article')
        equipment_line_element = etree.SubElement(product_element, 'EquipmentLine')
        title_element = etree.SubElement(product_element, 'Title')
        description_element = etree.SubElement(product_element, 'Description')
        manufacturer_element = etree.SubElement(product_element, 'Manufacturer')

        article_element.text = '' if article is None else article.strip()
        equipment_line_element.text = '' if equipment_line is None else equipment_line.strip()
        title_element.text = '' if title is None else title.strip()
        description_element.text = '' if description is None else description.strip()
        manufacturer_element.text = '' if manufacturer is None else manufacturer.strip()



async def create_elements(categories_ids: List[int],
                          internet_site_element: etree.Element,
                          brand_name: str,
                          exclude_108bit: bool):
    for main_category_id in categories_ids:
        main_category_title = await get_title_category(category_id=main_category_id)
        main_category_element = etree.SubElement(
            internet_site_element, 'Category',
            category_name=main_category_title,
        )
        products = await get_products(brand_name=brand_name,
                                      category_id=main_category_id,
                                      exclude_108bit=exclude_108bit)
        await create_products_elements(category_element=main_category_element, products=products)

        for data in await get_child_category(main_category_id):
            child_category_id = data.get('category_id')
            child_category_title = data.get('title')
            products = await get_products(brand_name=brand_name,
                                          category_id=child_category_id,
                                          exclude_108bit=exclude_108bit)
            if len(products) > 0:
                child_category_element = etree.SubElement(
                    main_category_element, 'Category',
                    category_name=child_category_title,
                )

                await create_products_elements(category_element=child_category_element, products=products)


async def create_tree(internet_sites: List[dict], brand_name: str, exclude_108bit: bool) -> etree.ElementTree:
    page = etree.Element('InternetSites')

    for data in internet_sites:
        internet_site_name = data.get('internet_site')
        categories_ids = data.get('categories_ids')
        internet_site_element = etree.SubElement(page, 'InternetSite', brand=internet_site_name)

        await create_elements(categories_ids=categories_ids,
                              internet_site_element=internet_site_element,
                              brand_name=brand_name,
                              exclude_108bit=exclude_108bit)

    doc = etree.ElementTree(page)
    return doc


async def create_xml(brand_name: str, exclude_108bit: bool):
    internet_sites_data = await search_main_data(brand_name=brand_name)

    xml_tree = await create_tree(internet_sites=internet_sites_data,
                                 brand_name=brand_name,
                                 exclude_108bit=exclude_108bit)

    xml_data = etree.tostring(xml_tree, pretty_print=True, xml_declaration=True, encoding='UTF-8')
    return xml_data
