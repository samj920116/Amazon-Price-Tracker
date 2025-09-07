import smtplib
from email.message import EmailMessage

class Email:
    def __init__(self, my_email:str,my_password:str):
        self.my_email = my_email
        self.my_password=my_password

    def send_alert_email(self,product_name:str, new_price:float, old_price:float):
        msg = EmailMessage()
        msg["Subject"] = "Low Price Alert!"
        msg["From"] = self.my_email
        msg["To"] = self.my_email

        body = f"Product: {product_name}\nCost now: {new_price}\n Old price:{old_price}"
        msg.set_content(body, charset="utf-8")

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(self.my_email, self.my_password)
            connection.send_message(msg)

    def send_error_mail(self):
        msg = EmailMessage()
        msg["Subject"] = 'No product data found!'
        msg["From"] = self.my_email
        msg["To"] = self.my_email

        body = '''Possible causes:
        1. Wrong URL, verify that the URL match the Amazon product.
        2. CSS selector need to be updated.
        3. Amazon bot detection -> Update the headers.'''
        msg.set_content(body, charset="utf-8")

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(self.my_email, self.my_password)
            connection.send_message(msg)
