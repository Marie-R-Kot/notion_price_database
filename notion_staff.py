from notion_client import Client

class NotionClient:
    

    def __init__(self, token: str, database_url: str) -> None:
        self.token = token
        self.client = Client(auth=self.token)
        self.database_id = database_url.split("/")[4].split("?")[0]


    def get_database_tag_ids(self) -> dict:
        """
        Return tags/properties ID's from database ID
        """
        data = self.client.databases.retrieve(self.database_id)["properties"]

        return {key: data[key]["id"] for key in data}
    

    def get_database_page_ids(self) -> list:
        """
        Return pages/main rows('title' id) ID's from database ID
        """
        rows = self.client.databases.query(database_id=self.database_id)["results"]

        return [row["id"] for row in rows]
    

    def get_database_page_ids_and_properties(self) -> dict:
        """
        Return pages ID's and tags/properties ID from database ID
        """
        pages = self.client.databases.query(database_id=self.database_id)["results"]
    
        final_pages =  {} 

        for row in pages:
            try:
                key=row['properties']['url']['rich_text'][0]['plain_text']
                final_pages[key] = row["id"]
            except (IndexError, KeyError):
                continue
        return final_pages
    

    def get_value_by_page_and_tag_ids(self,page_id: str, 
                                      tag_id: str, title: bool = False
                                      ) -> str:
        """
        Return exact value of property from choosed page
        """
        value = self.client.pages.properties.retrieve(page_id, tag_id)
        try:
            return value["results"][0]["title"]["plain_text"] if title else value[value["type"]]
        except IndexError:
            return None


    def change_prop_in_page(self, page_id: str, new_value: float, prop_id: str):
        '''
        Change number property
        '''
        try:
            self.client.pages.update(
            page_id=page_id,
            properties={
                #'byYE': {
                prop_id: {
                    'number': new_value
                    }
                }
            )

        except Exception:
            name = self.get_value_by_page_and_tag_ids(page_id, 'title', True)
            print(f"{name} price hasn't found")