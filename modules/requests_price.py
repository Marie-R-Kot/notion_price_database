"""Module provides opportunities to parse the price of products 
from popular supermarkets and specialized baking stores
"""

from time import sleep
from dataclasses import dataclass
from bs4 import BeautifulSoup
import requests

DELAY_BETWEEN_ATTEMPTS = 3

@dataclass
class Locator:
    """Class represents a locator
    One locator contains:
    element - type of parsed class
    value - parsed class name
    """
    element: str
    value: str


class PriceParser:
    """Class represents a parser for price from shop's site"""

    def __init__(self, user_agent: str, cookies: str) -> None:
        self.url = None
        self.domain = None
        self.locators = {
            "agrobar.org": Locator(
                "div",
                "js-product-price js-store-prod-price-val t-store__prod-popup__price-value",
            ),
            "spb.vkusvill.ru": Locator(
                "span", "js-datalayer-catalog-list-price hidden"
            ),
            "spb.tortomaster.ru": Locator("span", "price"),
            "lenta.com": Locator("p", "Price_secondaryPrice__ppVFT"),
            "www.perekrestok.ru": Locator("div", "price-card-unit-value"),
        }
        self.lenta_cookies = cookies
        self.user_agent = user_agent

    def get_price(self, url: str) -> float:
        """Function takes product page url and returns price in float format"""
        self.url = url
        self.domain = self.url.split("/")[2]
        sleep(DELAY_BETWEEN_ATTEMPTS)

        return self.get_price_value()

    def _get_html(self) -> str:
        headers = {
            "User-Agent": self.user_agent,
            "Accept": "text/html",
        }

        if self.domain == "lenta.com":
            headers["Cookie"] = self.lenta_cookies

        return requests.get(self.url, headers=headers, timeout=10).text

    def _format_price(self, price: str, replace_chars: dict, split_char: str) -> float:
        """The function removes currency symbols and extra spaces, converts commas to periods"""
        for old, new in replace_chars.items():
            price = price.replace(old, new)
        return float(price.split(split_char)[0])

    def get_price_value(self) -> float:
        """Function takes html, reforms it and finds price in parsed page using locator. 
        Extracted price is reformed to float format without special symbols"""

        response = self._get_html()
        bs = BeautifulSoup(response, "lxml")

        try:
            price = bs.find(
                self.locators[self.domain].element, self.locators[self.domain].value
            ).text
            if self.domain in [
                "www.vprok.ru",
                "agrobar.org",
                "spb.vkusvill.ru",
            ]:
                return self._format_price(price, {",": ".", " ": ""}, " ")

            if self.domain in ["spb.tortomaster.ru", "lenta.com"]:
                return self._format_price(price, {",": ".", " ": ""}, "₽")

            return self._format_price(price, {",": ".", " ": ""}, ".")

        except AttributeError:
            return 0.0
