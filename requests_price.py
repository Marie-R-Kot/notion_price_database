from bs4 import BeautifulSoup
import requests
from time import sleep

waits = 3

f1_dict = {
    'www.vprok.ru':'span',
    'agrobar.org':'div',
    'spb.vkusvill.ru' : 'span',
    'spb.tortomaster.ru': 'span',
    'lenta.com': 'p'
}
f2_dict = { # locators
    'www.vprok.ru':'Price_price__QzA8L Price_size_XL__MHvC1 Price_role_regular__X6X4D',
    'agrobar.org':'js-product-price js-store-prod-price-val t-store__prod-popup__price-value',
    'spb.vkusvill.ru': 'js-datalayer-catalog-list-price hidden',
    'spb.tortomaster.ru': 'price',
    'lenta.com': 'Price_secondaryPrice__ppVFT'
    }


def get_price(url: str) -> str:

    def _get_html(url: str) -> str:

        if (url.split('/')[2]=='lenta.com'):
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0",
                "Accept": "text/html",
                "Cookie": 'ASP.NET_SessionId=0ut5krvg5t5dyv3ys0of3j0g; GACustomerId=c35df804b0284c1b89ca1c5589a2da57; .ASPXANONYMOUS=vM4yXuC1SJS7Dlk-j-oGbufuQE88A-mCtK8vCkxB4ChJypxqV9YpGaxQK7h8dXMFBAhftarNA3QhY72TRpisyO_q5ejG0wUKBGMqUwauMz3l-SbUFjQvjB55GiW09d-0t5Qj1A2; CustomerId=5b27bcf2434c48f79cde91acc2a87463; LNCatalogRoot=true; LNProduct=true; LNStart=true; LNCatalogNodes=true; IsNextSiteAvailable=True; KFP_DID=2d15ae84-85ea-5f34-c783-09f12503531e; UnAuthorizedNavigationsCount=3; AuthorizationMotivationHidden=true; oxxfgh=17b09ea5-9676-4a4b-a712-ed262a3bb91a#0#5184000000#5000#1800000#44965; CityCookie=spb; CitySubDomainCookie=spb; ShouldSetDeliveryOptions=False; ValidationToken=9552c564095f34dcba8285e3d2c84b67; StoreSubDomainCookie=0011; Store=0011; DeliveryOptions=Pickup; LastUpdate=2024-06-14; DontShowCookieNotification=False; qrator_jsid=1718388306.108.NcKXtQ5oVhYLPHe2-lnmistjh15419nhtjuf6agfe01vnc85g; cookiesession1=678B286F60CEF685914417AA98287BB3; ReviewedSkus=706256,068115,634877,058021,006128,665644,150743,003951,520163,206048,070908,671166'
                }

        else: 
            headers = {
                "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                "Accept": "text/html"
                }
        return requests.get(url, headers=headers).text


    def _get_price_value() -> str:

        def process_price(price: str, replace_chars: dict, split_char: str) -> float:
            for old, new in replace_chars.items():
                price = price.replace(old, new)
            return float(price.split(split_char)[0])
    
        response = _get_html(url)
        bs = BeautifulSoup(response,"lxml")
        domain = url.split('/')[2]

        try:
            price = bs.find(f1_dict[domain], f2_dict[domain]).text
            if domain in [
                'www.vprok.ru',
                'agrobar.org',
                'spb.vkusvill.ru',
            ]:
                return  process_price(price, {',': '.', ' ': ''}, ' ')

            elif domain in ['spb.tortomaster.ru', 'lenta.com']:
                return process_price(price, {',': '.', ' ': ''}, '₽')

        except AttributeError: 
            return None

    sleep(waits)
    result = _get_price_value()

    return result
