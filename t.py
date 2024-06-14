import pandas as pd
from requests_price import *
from notion_staff import *
import os

os.system("cls" if os.name == "nt" else "clear")  # clear terminal window

TOKEN = "secret_qpAS6oTspiFNSXoTVvWNXhtXYNhwmP949mDNOBN4T1x"
database_url = 'https://www.notion.so/kot-bloknot/9ad4a802ee6b49bf9dfb7bf5a74444a5?v=f544e39eebed4ca1b92b17735c1559b7' #Выпекот
#database_url = 'https://www.notion.so/kot-bloknot/55e7ebfbf6514753b9b588370a1e12f4?v=774ece5e961740cdab81e97acc645779'

notion = NotionClient(TOKEN, database_url)

props_id = notion.get_database_tag_ids()
pages_id = notion.get_database_page_ids_and_properties()
print(props_id)  

Base = pd.DataFrame(data=pages_id.keys(),columns=['url'])
Base['page_id'] = pd.DataFrame(data=pages_id.values())

Base['price'] = Base['url'].apply(get_price)

for count in range(len(Base)):
    notion.change_price_in_page(Base['page_id'].iloc[count],Base['price'].iloc[count])
