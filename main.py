import requests
from bs4 import BeautifulSoup


DISCORD_WEBHOOK = "DISCORD_WEBHOOK_HERE"

# See My HTTP Headerat : "http://myhttpheader.com"
URL = "https://www.amazon.de/-/en/76903/dp/B08WWZJ8G4/ref=sr_1_1?keywords=lego+speed+champions" \
      "&qid=1645795393&sprefix=lego+speed%2Caps%2C121&sr=8-1"
HEADER = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                  "Version/14.0.3 Safari/605.1.15",
    "Accept-Language": "en-us"
}

CURRENCIES = ["€", "$"]
EXPECTED_PRICE = 39.99

response = requests.get(URL, headers=HEADER)
soup = BeautifulSoup(response.content, "lxml")

# Get array of price within the class a-offscreen
price_list = soup.find_all("span", {"class": "a-offscreen"})
price = price_list[0].get_text()
print(f"Price: {price}")

# Get product title
title = soup.find(id="productTitle").get_text().strip()
print(title)

# Clean data
currency = None
for i in price:
    for c in CURRENCIES:
        # Check for currency symbol
        if i == c:
            currency = "€"
            break

# Remove currency symbol
price = price.replace(currency, "")
# Remove comma
price = price.replace(",", "")

print(f"Currency: {currency}, Price: {price}")

# Convert price to float
price_as_float = float(price)

# Compare price
if price_as_float < EXPECTED_PRICE:
    pct_discount = (1 - price_as_float / EXPECTED_PRICE) * 100
    message = f"{title} is now {currency}{price} ⬇️ {round(pct_discount, 2)}% lower than your watch price 💶"
    print(f"Final message: {message}")

    data = {"content": message}
    response = requests.post(DISCORD_WEBHOOK, json=data)
    print(f"Discord response: {response}")
