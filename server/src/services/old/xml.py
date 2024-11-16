import logging
from typing import Optional

from lxml import etree
from sqlalchemy import select

from src.database import get_session
from src.models import Manufacturer, Product
from src.services.db_query import get_products_for_categories_108bit

logger = logging.getLogger('server')


def get_brands_id():
    with get_session() as session:
        return session.execute(select(Manufacturer.id, Manufacturer.name)).all()

def filling_products_exclude_108bit(products_element, brand_id: int, product_108bit_ids):
    count_product = 0
    manufacturer: Optional[str] = None
    with get_session() as session:
        products = session.execute(select(Product).where(Product.manufacturer_id == brand_id)).scalars()
        for product in products:
            if product.id in product_108bit_ids:
                continue
            product_element = etree.SubElement(products_element, 'Product')

            manufacturer = etree.SubElement(product_element, 'Manufacturer')
            manufacturer.text = product.manufacturer.name
            manufacturer = product.manufacturer.name

            article = etree.SubElement(product_element, 'Article')
            title = etree.SubElement(product_element, 'Title')

            description = etree.SubElement(product_element, 'Description')
            if product.product_description is None:
                title.text = ''
                description.text = ''
            else:
                description.text = product.product_description.description
                title.text = product.product_description.title
            # title.text = product.product_description.title
            article.text = product.article
            # description.text = product.product_description.description

            count_product = count_product + 1

    logger.info(f'Count products exclude 108bit: {count_product}, manufacturer: {manufacturer}')

def filling_products(products_element, brand_id: int):
    count_product = 0
    with get_session() as session:
        products = session.execute(select(Product).where(Product.manufacturer_id == brand_id)).scalars()
        for product in products:
            product_element = etree.SubElement(products_element, 'Product')

            manufacturer = etree.SubElement(product_element, 'Manufacturer')
            manufacturer.text = product.manufacturer.name
            manufacturer = product.manufacturer.name

            article = etree.SubElement(product_element, 'Article')
            title = etree.SubElement(product_element, 'Title')

            description = etree.SubElement(product_element, 'Description')
            if product.product_description is None:
                title.text = ''
                description.text = ''
            else:
                description.text = product.product_description.description
                title.text = product.product_description.title

            article.text = product.article

            count_product += 1

    logger.info(f'Count products: {count_product}, manufacturer: {manufacturer}')
            # attributes = etree.SubElement(product_element, 'Attributes')
            # for attribute in product.attributes:
            #     etree.SubElement(attributes, 'Attribute',
            #                      folder=attribute.name,
            #                      filename=attribute.value)

            # images = etree.SubElement(product_element, 'Images')
            # for image in product.images:
            #     etree.SubElement(images, 'Image',
            #                      folder=image.image.folder,
            #                      filename=image.image.filename)

            # documents = etree.SubElement(product_element, 'Documents')
            # for document in product.documents:
            #     etree.SubElement(documents, 'Document',
            #                      folder=document.document.folder,
            #                      filename=document.document.filename)



def get_xml_all_catalog():
    brands = get_brands_id()
    root = etree.Element('Products')
    for brand_id, brand_name in brands:
        # page = etree.SubElement(root, 'Products')
        filling_products(products_element=root, brand_id=brand_id)

    xml_data = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8')
    return xml_data


async def get_xml_catalog_exclude_108bit():
    products_108bit_ids = await get_products_for_categories_108bit()
    brands = get_brands_id()
    root = etree.Element('Products')
    for brand_id, brand_name in brands:
        # page = etree.SubElement(root, 'Products')
        filling_products_exclude_108bit(products_element=root,
                                        brand_id=brand_id,
                                        product_108bit_ids=products_108bit_ids)

    xml_data = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8')
    return xml_data