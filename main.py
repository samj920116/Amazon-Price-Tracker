from amazon_manager import AmazonTracker
from csv_manager import CSVManager
from email_manager import Email
import os
from dotenv import load_dotenv

load_dotenv()

#From .env file:
MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PSW")


# Amazon product URL and selectors used to fetch price and name.
AMAZON_URL = "https://www.amazon.com.mx/SAMSUNG-Galaxy-Ultra-Negro-512GB/dp/B0DNTWTCLZ/?_encoding=UTF8&pd_rd_w=R9ZMd&content-id=amzn1.sym.802f54ee-e822-4638-95e2-f48ad27398f5&pf_rd_p=802f54ee-e822-4638-95e2-f48ad27398f5&pf_rd_r=CYDNCB0NKXA0FWD65F58&pd_rd_wg=e8EXs&pd_rd_r=7b6e16ac-872d-498e-98b8-e0247bc418a5&ref_=pd_hp_d_atf_unk&th=1"
PRICE_WHOLE_SELECTOR = "span.a-price-whole"
PRICE_FRACTION_SELECTOR = "span.a-price-fraction"
PRODUCT_NAME_SELECTOR = "span#productTitle"


csv = CSVManager()
min_price = csv.get_min_price()

email = Email(my_email=MY_EMAIL, my_password=MY_PASSWORD)

amazon_tracker = AmazonTracker(url=AMAZON_URL,
                               min_price=min_price,
                               name_selector=PRODUCT_NAME_SELECTOR,
                               price_selectors=(PRICE_WHOLE_SELECTOR, PRICE_FRACTION_SELECTOR))

action = amazon_tracker.check_price()
if action == "Update":
    csv.update_min_price(name=amazon_tracker.product_name,
                         price=amazon_tracker.price)
elif action == "Error":
    email.send_error_mail()
elif action == "Alert":
    email.send_alert_email(product_name=amazon_tracker.product_name,
                           new_price=amazon_tracker.price,
                           old_price=amazon_tracker.min_price)
    csv.update_min_price(name=amazon_tracker.product_name,
                         price=amazon_tracker.price)
else:
    print("No action needed. Price is higher than min_price.")