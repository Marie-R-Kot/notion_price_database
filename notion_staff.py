from notion_client import Client

TOKEN = "secret_qpAS6oTspiFNSXoTVvWNXhtXYNhwmP949mDNOBN4T1x"
notion = Client(auth=TOKEN)

def get_database_tag_ids(database_id: str) -> dict:
    data = notion.databases.retrieve(database_id)["properties"]

    properties =  {} 

    for key in data:
        properties[key] = data[key]["id"]
    return properties


def get_database_row_ids(database_id: str) -> list:
    """
    Возвращаем ID дочерних страниц базы по ID базы.
    Фильтр пока закомментирован, потом можно прикрутить и в параметр вывести.
    """
    rows = notion.databases.query(
        **{
            "database_id": database_id,
        } 
    )["results"]

    return [row["id"] for row in rows]

def get_database_page_ids_and_properties(database_id: str) -> dict:
    """
    Возвращаем ID дочерних страниц базы по ID базы.
    """
    pages = notion.databases.query(
        **{
            "database_id": database_id,
        } 
    )["results"]
    
    final_pages =  {} 

    for row in pages:
        try:
            key=row['properties']['url']['rich_text'][0]['plain_text']
            final_pages[key] = row["id"]
        except IndexError:
            continue
    return final_pages

def get_value_by_page_and_tag_ids(
    page_id: str, tag_id: str, title: bool = False
) -> str:
    """
    Берём ID дочерней страницы и ID тэга, получаем значение тэга
    * ID дочерней страницы брать в get_database_row_ids()
    * ID тэга брать в get_database_tag_ids()
    """
    value = notion.pages.properties.retrieve(page_id, tag_id)
    try:
        if title:
            return value["results"][0]["title"]["plain_text"]
        else:
            return value[value["type"]]
    except IndexError:
        return None


def get_database_id_from_url(url: str) -> str:
    return url.split("/")[4].split("?")[0]


def get_page_id_from_url(url: str) -> str:
    return url.split("-")[-1]


def change_price_in_page(page_id: str, new_value: float):
    #UPDATE number property
    try:
        notion.pages.update(page_id=page_id,
                            **{"properties": {
                                            'nQZg' : { 
                                            #'byYE': {
                                            'number': new_value
                                            }
                                        }  
                            } 
                            )
    except Exception:
        name = get_value_by_page_and_tag_ids(page_id, 'title', True)
        print(f"{name} price hasn't found")
        