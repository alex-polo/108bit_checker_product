from lxml import etree
from lxml.etree import SubElement

from src import tools
from src.services.db_query import get_108bit_main_categories, get_108bit_sub_categories


async def set_categories(categories_element: SubElement):
    for pk_key_main_cat, title_main_cat in await get_108bit_main_categories():
        main_category_element = etree.SubElement(categories_element, "category", id=str(pk_key_main_cat))
        main_category_element.text = title_main_cat
        for pk_key_sub_cat, title_sub_cat in await get_108bit_sub_categories(category_id=pk_key_main_cat):
            sub_category_element = etree.SubElement(categories_element, "category",
                                                    id=str(pk_key_sub_cat),
                                                    parentId=str(pk_key_main_cat))
            sub_category_element.text = title_sub_cat


async def get_yml_categories():
    root = etree.Element('yml_catalog', date=tools.get_current_time())
    shop = etree.SubElement(root, "shop")

    etree.SubElement(shop, "name").text = "108БИТ"
    etree.SubElement(shop, "company").text = '108БИТ Парсер'
    etree.SubElement(shop, "url").text = ""

    # Добавляем валюты
    currencies = etree.SubElement(shop, "currencies")
    etree.SubElement(currencies, "currency", id="RUB", rate="1")

    # Добавляем категории
    categories = etree.SubElement(shop, "categories")
    await set_categories(categories_element=categories)


    xml_data = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8')
    return xml_data