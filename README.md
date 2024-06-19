# notion_price_database
Parse prices to DataFrame and update Notion database

Program contains two implemented modules and example of its usage for parsing price from popular supermarkets and special bakery shops, creating DataFrame with connection of url, link to page in Notion and parsed price, than updating price in database

### Required install
- notion_client
- requests
- BeautifulSoup
- pandas
- PyYAML

### Preparation
Before try to run example you need to create a Notion database and fill it with products, its price you want to know. 
Need to create at least three columns. First - title will  ce created automatically, while you create database, you may fill it with name of products. For each row in this column Notion will create a new page. Further information from this column will be indicated by pages. 
Second column will have property name "url" and will contains link to parsed product. Third column will have property name "Price" and will be filled with parsed price later
![](/assets/images/electrocat.png)


### Configuration information
Before starting the programm they need to fill TOKEN from notion, database url and name of naumber proprety, that need to be changed, in main.py

Need to change lenta cookies before starting the program in requests_price.py