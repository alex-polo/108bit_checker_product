from lxml import etree

from src import tools
from src.services.db_query import get_images_for_product, get_attrs_for_product, get_documents_for_product


def get_main_yml_element() -> tuple:
    root = etree.Element('yml_catalog', date=tools.get_current_time())
    shop = etree.SubElement(root, "shop")

    etree.SubElement(shop, "name").text = "108БИТ"
    etree.SubElement(shop, "company").text = '108БИТ Парсер'
    # etree.SubElement(shop, "url").text = ""

    # Добавляем валюты
    currencies = etree.SubElement(shop, "currencies")
    currency_rub = etree.SubElement(currencies, "currency", id="RUB", rate="1")
    # currency_usd = etree.SubElement(currencies, "currency", id="USD", rate="60")

    return root, shop


async def set_images(product_id: int, element=etree.SubElement):
    images_element = etree.SubElement(element, "images")
    for product_image_name, file_uuid in await get_images_for_product(product_id=product_id):
        etree.SubElement(images_element, "image", uuid=str(file_uuid)).text = product_image_name


async def set_attrs_product(product_id: int, element=etree.SubElement):
    documents_element = etree.SubElement(element, "attributes")
    for attribute_name, attribute_value in await get_attrs_for_product(product_id=product_id):
        attr_element = etree.SubElement(documents_element, "attribute")
        etree.SubElement(attr_element, "name").text = attribute_name
        etree.SubElement(attr_element, "value").text = attribute_value


async def set_documents(product_id: int, element=etree.SubElement):
    documents_element = etree.SubElement(element, "documents")
    for product_document_name, storage_uuid in await get_documents_for_product(product_id=product_id):
        etree.SubElement(documents_element, "document", uuid=str(storage_uuid)).text = product_document_name