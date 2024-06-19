"""
Contains example of usage for implemented notion_database and request_price modules

Get url of products from Notion database and create DataFrame that connects url and 
link to page in database, then parse it's price and update it in Notion

NOTE: If price can't be found, price in Notion database will remain unchanged
All products without price will be output to console

Please refer to README.md for detailed information and guide for filling config.yaml
"""

import os
import yaml
import pandas as pd
from modules.notion_database import NotionClient
from modules.requests_price import PriceParser


class Config:
    """Read configuration file"""

    def __init__(self, filename: str):

        with open(filename, encoding="utf-8") as f:
            cfg = yaml.load(f, Loader=yaml.FullLoader)

        self.token = cfg["token"]
        self.database_url = cfg["database_url"]
        self.prop_to_change = cfg["property_to_change"]
        self.user_agent = cfg["user_agent"]
        self.lenta_cookies = cfg["lenta_cookies"]


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")

    # Read configuration file
    config = Config("config.yaml")
    # Create a notion variable that relates to our database
    notion = NotionClient(config.token, config.database_url)

    # Get id's for every properties/columns
    props_id = notion.get_database_prop_ids()
    # Get id's of main page (property id 'title') and content in 'url' property
    pages_id = notion.get_database_page_ids_and_property()

    # Create DataFrame that contains page ids and url of products
    df = pd.DataFrame({"url": pages_id.keys(), "page_id": pages_id.values()})

    # Add new column to DataFrame that contains parsed price of product from url
    df["price"] = df["url"].apply(PriceParser(config.user_agent, config.lenta_cookies).get_price)

    # Change price in Notion database, update number in column from config file (prop_to_change)
    for count in range(len(df)):
        page_id = df["page_id"].iloc[count]
        price = df["price"].iloc[count]
        notion.change_prop_in_page(page_id, price, props_id[config.prop_to_change])
