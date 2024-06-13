from bs4 import BeautifulSoup
import requests


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
    'lenta.com': 'Price_mainPrice__T9yBp'
}


def get_price(url: str) -> str:

    def _get_html(url: str) -> str:
        
        if (url.split('/')[2]=='lenta.com'):
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0",
                "Accept": "text/html",
                "Cookie": "ASP.NET_SessionId=0ut5krvg5t5dyv3ys0of3j0g; GACustomerId=c35df804b0284c1b89ca1c5589a2da57; qrator_jsid=1718042092.210.gPbIipb12SleL84f-mhslj6k6g0mc7kj1jvipnet1od4ljsm5; .ASPXANONYMOUS=vM4yXuC1SJS7Dlk-j-oGbufuQE88A-mCtK8vCkxB4ChJypxqV9YpGaxQK7h8dXMFBAhftarNA3QhY72TRpisyO_q5ejG0wUKBGMqUwauMz3l-SbUFjQvjB55GiW09d-0t5Qj1A2; CustomerId=5b27bcf2434c48f79cde91acc2a87463; LNCatalogRoot=true; LNProduct=true; LNStart=true; LNCatalogNodes=true; ShouldSetDeliveryOptions=True; IsNextSiteAvailable=True; LastUpdate=2024-06-10; ValidationToken=9d60dc53f2f2e749e73e5e65c6e7de40; KFP_DID=2d15ae84-85ea-5f34-c783-09f12503531e; ReviewedSkus=293862,311362,383728,094429,011458,270863,011225,525353,375708,614931,455088; cookiesession1=678B286F1C392B112C8B70E143C36EDC; UnAuthorizedNavigationsCount=3; DontShowCookieNotification=true; oxxfgh=L!0a0e1252-b66b-42d4-f233-4817837ba918#1#1800000#5000#1800000#44965; AuthorizationMotivationHidden=true; .AspNet.ApplicationCookie=5CFpV0bMobGlS6tL9k7hmDkh7qdYhNf7khhkG5RQfSsuxIlci87vwPRj2P3R4gs3srqAJ36xOLf7_aW3KTJRgQl36KcSwiUWtccfoZsbdkyQOAYWigA0xX6BAtSn1J1A0iSVCJbozNOM-mbrTHO4fST9LbqS1rrIA8GA8hUMNDZ0Ei2OyZDD7lQD1mvrq5-8a8IPXIMKwtroII87QsDkxbgiL7673Hy9lGign3laSuck9TxLiP_3lrsThcaYIOHdJji0cYiV36x11NHgj-dxMzaBF9AUnRos_T30YiDtI10h-S1y1oCdGw5t-QHexNaPtuKXe7ojwnSneLBGkRmvArGLe2Xa3I3aVGW4UNvYHIVhg3tqhn4EMGh1N31fEOClUAsruoF_e9S3rUSoEh23CszPVfaWnHgUtJMcEx94xSYp8zT5w-p5F6tv7JlxNtQ_NThZ5jTHpbRFLl7v98W9JNIwGSYA7lbvqRmFzp-IBQq9oNUWnglSV1dvzualiQQ8e4Yz945sn1PdzC5AgUUj-UADyxJWib5yra90cOYUH1uOej25d89ycWNXL97QL9Dp6dc2j1mWot0p36Iru2tVy8IAmkWJzZAEtizPrZPMrujRnnvVrmv5-pS3hQOkwwL1bFsy9YmQddUoMez_Y2JRHiJeJ7jJIfsBhgfdHYm6IM18Iwz0LVVdqoozqHsmV8uh9kV6XmlPVpaIdX_AEgQUkLSS8iNC9Rad6zW1WZWrBdF1e7Qxp2ePcNopyqTKjBD7Ley6uCMeyXy-htCvKZWbUsm_dyY6DLKHYSwYv2Um5scpsYSH"
                }

        else: 
            headers = {
                "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                "Accept": "text/html"
                }
        return requests.get(url, headers=headers).text
        
        
    def _get_price_value() -> str:
        response = _get_html(url)
        bs = BeautifulSoup(response,"lxml")

        try:
            if (url.split('/')[2]=='www.vprok.ru') or (url.split('/')[2]=='agrobar.org') or (url.split('/')[2]=='spb.vkusvill.ru'):
                # if url.split(lalala) in {www.vprok, www.yok}
                price = bs.find(f1_dict[url.split('/')[2]], f2_dict[url.split('/')[2]]).text
                return float(price.replace(',','.').split(' ',-1)[0])
            
            elif (url.split('/')[2]=='spb.tortomaster.ru') or (url.split('/')[2]=='lenta.com'):
                price = bs.find(f1_dict[url.split('/')[2]], f2_dict[url.split('/')[2]]).text
                return float(price.replace(',','.').replace(' ','').split('₽')[0])
          
        except AttributeError: 
            return None
    
    result = _get_price_value()

    return result
