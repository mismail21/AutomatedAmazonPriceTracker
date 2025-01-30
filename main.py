import requests
from bs4 import BeautifulSoup
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

SMTP_addr = os.getenv("SMTP_ADDRESS")
email_addr = os.getenv("EMAIL_ADDRESS")
email_pass = os.getenv("EMAIL_PASSWORD")


url = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"

response = requests.get(url)

website_html = response.content

soup = BeautifulSoup(website_html, "html.parser")


price = soup.find(class_="a-offscreen").getText()

price_without_currency = price.split("$")[1]
float_price = float(price_without_currency)

target = 70



title = soup.find(id="productTitle").get_text().strip()
print(title)




if float_price < target:
    message = f"{title} is on sale for {price}!"

    with smtplib.SMTP(SMTP_addr, port=587) as connection:
        connection.starttls()
        result = connection.login(email_addr, email_pass)
        connection.sendmail(
            from_addr=email_addr,
            to_addrs=email_addr,
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{url}".encode("utf-8")
        )

