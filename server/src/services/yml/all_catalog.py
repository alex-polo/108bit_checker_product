import logging

from lxml import etree
from lxml.etree import Element

from src import tools
from src.services.db_query import (
    get_108bit_main_categories,
    get_108bit_sub_categories,
    get_products_for_categories,
    get_all_id_108bit_categories,
    get_desc_for_product,
    get_manufacturer_for_product,
    get_images_for_product,
    get_documents_for_product,
    get_attrs_for_product
)
from src.services.yml.elements import get_main_yml_element, set_images, set_attrs_product, set_documents

logger = logging.getLogger('server')

async def set_categories(categories_element):
    for pk_key_main_cat, title_main_cat in await get_108bit_main_categories():
        main_category_element = etree.SubElement(categories_element, "category", id=str(pk_key_main_cat))
        main_category_element.text = title_main_cat
        for pk_key_sub_cat, title_sub_cat in await get_108bit_sub_categories(category_id=pk_key_main_cat):
            sub_category_element = etree.SubElement(categories_element, "category",
                                                    id=str(pk_key_sub_cat),
                                                    parentId=str(pk_key_main_cat))
            sub_category_element.text = title_sub_cat


# async def set_images(product_id: int, element: Element):
#     images_element = etree.SubElement(element, "images")
#     for product_image in await get_images_for_product(product_id=product_id):
#         etree.SubElement(images_element, "image").text = product_image


# async def set_documents(product_id: int, element: Element):
#     documents_element = etree.SubElement(element, "documents")
#     for product_document in await get_documents_for_product(product_id=product_id):
#         etree.SubElement(documents_element, "document").text = product_document
#
#
# async def set_attrs_product(product_id: int, element: Element):
#     documents_element = etree.SubElement(element, "attributes")
#     for attribute_name, attribute_value in await get_attrs_for_product(product_id=product_id):
#         attr_element = etree.SubElement(documents_element, "attribute")
#         etree.SubElement(attr_element, "name").text = attribute_name
#         etree.SubElement(attr_element, "value").text = attribute_value


async def set_offers(offers_element):
    quantity_products = 0
    for category_id in await get_all_id_108bit_categories():
        for product in await get_products_for_categories(category_id=category_id):
            product_title, product_description = await get_desc_for_product(product_id=product.id)
            manufacturer = (await get_manufacturer_for_product(product_id=product.id))[0]


            offer_product = etree.SubElement(offers_element, "offer", id=str(product.id), available="true")
            etree.SubElement(offer_product, "url").text = product.url
            etree.SubElement(offer_product, "categoryId").text = str(category_id)
            etree.SubElement(offer_product, "price").text = "0"
            etree.SubElement(offer_product, "quantity").text = "0"
            etree.SubElement(offer_product, "currencyId").text = "RUB"
            etree.SubElement(offer_product, "name").text = product_title
            etree.SubElement(offer_product, "description").text = product_description
            etree.SubElement(offer_product, "manufacturer").text = manufacturer

            await set_attrs_product(product_id=product.id, element=offer_product)
            await set_images(product_id=product.id, element=offer_product)
            await set_documents(product_id=product.id, element=offer_product)

            quantity_products += 1
    logger.info(f'Quntity products: {quantity_products}')


async def get_yml_all_catalog():
    root, shop = get_main_yml_element()

    # Добавляем валюты
    # currencies = etree.SubElement(shop, "currencies")
    # currency_rub = etree.SubElement(currencies, "currency", id="RUB", rate="1")
    # currency_usd = etree.SubElement(currencies, "currency", id="USD", rate="60")

    # Добавляем категории
    categories = etree.SubElement(shop, "categories")
    await set_categories(categories_element=categories)

    # Добавляем продукты
    offers = etree.SubElement(shop, "offers")
    await set_offers(offers_element=offers)
    xml_data = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8')
    return xml_data