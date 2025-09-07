# Description
Tracks an Amazon product price, evaluating the price history stored, and if the price is the lowest, an email notification is sent.

# Configuration
1. Create a file called .env
2. Add your information into .env file. **Be careful, if your email is not gmail, update the provider in email_manager.py -> EMAIL_SERVER**
```txt
MY_EMAIL="your_email@gmail.com"
MY_PSW="PswObteinedFromYourMailServer"
RECEIVER_EMAIL="email_for_notification@mail.com"
```
3. Into main.py update the constant AMAZON_URL with the link to the product you want to track.

# Errors
If the product information couldn't be fetch, an error email will be sent.  

