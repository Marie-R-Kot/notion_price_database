# notion_price_database
Parse prices to DataFrame and update Notion database

Program contains two implemented modules and an example of its usage.
The main purpose is to update prices in Notion database. For which prices are parsed from popular supermarkets (lenta.com, perekrestok.ru, vkusvill.ru) and special bakery shops (tortomaster.ru, agrobar.org). Then DataFrame is created to establish a connection between price, product url and link to Notion. Finally, price is loaded in database

### Required install
- notion_client
- requests
- BeautifulSoup
- pandas
- PyYAML

### Preparation in Notion
Before try to run example, you need to create a Notion database and fill it with products, its price you want to know. 
Need to create at least three columns. 
* First - title will be created automatically, while you create database, you may fill it with name of products. 
    * For each row in this column Notion will create a new page. Further information from this column will be indicated by pages. 
* Second column will have property name "url" and will contains link to parsed product.
* Third column will have property name "Price" and will be filled with parsed price later.
  
![](/assets/images/Notion.jpg)

Check that your database is not private and placed in Workspace!

### Configuration information
Before starting the program you need to fill all blank lines in config.yaml
It contains:
- token formatting 'secret{your_clue}'
  - To get your token read https://developers.notion.com/docs/authorization
- database url formatting 'https://www.notion.so/{workspace_name}/{database_id}?v={view_id}'
- property_to_change 'Name of numeric column you want to change'
- lenta_cookies
  - To get cookies go to lenta.com, choose any product and open its page, press F12. Go to Network, update page with Ctrl + R. Choose first page in Name. Then look for Cookies in Headers - Request Headers in right window. Copy this long line into configuration file