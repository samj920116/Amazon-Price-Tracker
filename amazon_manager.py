from bs4 import BeautifulSoup
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import re
#Header information get it from https://myhttpheader.com/:
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "es-419,es;q=0.9,es-ES;q=0.8,en;q=0.7,en-GB;q=0.6,en-US;q=0.5,es-MX;q=0.4",
    "Priority": "u=0, i",
    "Sec-Ch-Ua": "\"Microsoft Edge\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0",
}
class AmazonTracker:
    def __init__(self, url:str, min_price:float, name_selector:str,price_selectors: tuple[str,str]):
        self.price = 0
        self.min_price = min_price
        self.product_name = None
        self.url = url
        self.session = None
        self.name_selector = name_selector
        self.price_selectors = price_selectors

        self.make_session()

    def get_product_data(self)->str:
        response = self.session.get(self.url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        name = soup.select_one(self.name_selector)
        price_whole = soup.select_one(self.price_selectors[0])
        price_fraction = soup.select_one(self.price_selectors[1])

        if name is None or price_whole is None or price_fraction is None:
            output = "No Data found"
        else:
            name = name.get_text()
            name = re.sub(r'\s+', ' ', name)
            name = name.replace(',', '')
            self.product_name = name
            self.price = float(price_whole.get_text().replace(",", "") + price_fraction.get_text())
            output = f"{self.product_name}\n(${self.price})"
        return output

    def make_session(self)->None:
        s = requests.Session()
        s.headers.update(HEADERS)
        retry = Retry(
            total=3, backoff_factor=0.6,
            #429-Too Many Requests, 500-Internal Server Error, 502-Bad Gateway, 503-Service Unavailable,504-Gateway Timeout
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=("GET", "HEAD"),
            raise_on_status=False,
        )
        s.mount("https://", HTTPAdapter(max_retries=retry))
        s.mount("http://", HTTPAdapter(max_retries=retry))
        self.session =  s

    def check_price(self)->str:
        """
        Compare the Amazon product price with the min price to returns the action to be taken.
            - Update: Just update the min price in CSV file.
            - Error: Send an email to request developer to update the selectors.
            - Alert: Send an email warning a new lower price. And update the CSV file.

        Returns:
            String with command of next action to be taken.
            Internal variables are updated
        """
        action_required = None
        if self.get_product_data() == "No Data found":
            action_required="Error"
        elif self.min_price == 0:
            action_required = "Update"
        elif self.price < self.min_price:
            action_required = "Alert"
        return action_required
