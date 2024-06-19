"""Module provides class for working with Notion databases: extract information from database
and change numeric property in database
"""

from notion_client import Client


class ParsingException(Exception):
    """Class represents new exception type for price that can't be parsed"""


class NotionClient:
    """Class contains functions to get information from Notion database 
    with token and database url"""

    def __init__(self, token: str, database_url: str) -> None:
        self.token = token
        self.client = Client(auth=self.token)
        self.database_id = database_url.split("/")[4].split("?")[0]

    def _check_number(self, number):
        if number == 0.0:
            raise ParsingException("Number hasn't found")

    def get_database_prop_ids(self) -> dict:
        """
        Return properties ID's from database ID
        Return dict: key - name of property, value - id
        """
        data = self.client.databases.retrieve(self.database_id)["properties"]

        return {key: data[key]["id"] for key in data}

    def get_database_page_ids(self) -> list:
        """
        Return pages/main rows('title' id) ID's from database ID
        """
        rows = self.client.databases.query(database_id=self.database_id)["results"]

        return [row["id"] for row in rows]

    def get_database_page_ids_and_property(self) -> dict:
        """
        Return pages ID's and properties ID from database ID
        Return dict: key - url, value - page id
        """
        pages = self.client.databases.query(database_id=self.database_id)["results"]

        final_pages = {}

        for row in pages:
            try:
                key = row["properties"]["url"]["rich_text"][0]["plain_text"]
                final_pages[key] = row["id"]
            except (IndexError, KeyError):
                continue
        return final_pages

    def get_value_by_page_and_prop_ids(
        self, page_id: str, prop_id: str, title: bool = False
    ) -> str | None:
        """
        Return exact value of property from choosed page
        """
        value = self.client.pages.properties.retrieve(page_id, prop_id)
        try:
            return (
                value["results"][0]["title"]["plain_text"]
                if title
                else value[value["type"]]
            )
        except IndexError:
            return None

    def change_prop_in_page(self, page_id: str, new_value: float, prop_id: str):
        """
        Change number property
        """
        try:
            self._check_number(new_value)
            self.client.pages.update(
                page_id=page_id, properties={prop_id: {"number": new_value}}
            )

        except ParsingException:
            name = self.get_value_by_page_and_prop_ids(page_id, "title", True)
            print(f"{name} price hasn't found")
