import pandas as pd
from requests_price import *
from notion_staff import *
import os

os.system("cls" if os.name == "nt" else "clear")  # clear terminal window

TOKEN = ""
database_url = '' 
prop_to_change = "Цена"

notion = NotionClient(TOKEN, database_url)

props_id = notion.get_database_tag_ids()
pages_id = notion.get_database_page_ids_and_properties()
print(props_id)  

Base = pd.DataFrame(data=pages_id.keys(),columns=['url'])
Base['page_id'] = pd.DataFrame(data=pages_id.values())

Base['price'] = Base['url'].apply(get_price)

for count in range(len(Base)):
    page_id = Base['page_id'].iloc[count]
    price = Base['price'].iloc[count]
    notion.change_prop_in_page(page_id, price, props_id[prop_to_change])
