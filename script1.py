import requests
import re
import mysql.connector
from bs4 import BeautifulSoup

#defining mysql variables
mHost = "localhost"
mUser = "root"
mPassword = "root"
mDatabase = "jeans"

rootUrl= ''
itemUrl = ''
itemPID = ''
itemName = ''
itemPrice = 0.00

def scrape():
    url = "https://oldnavy.gap.com/browse/product.do?pid=846874002&vid=1&pcid=85729&cid=85729&nav=meganav%3AWomen%3AWomen%27s+Bottoms%3AJeans#pdp-page-content"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    #stores page title, usually includes item name
    itemName = (soup.title.string)

    #finds item URL
    itemUrl = soup.find("link", rel="canonical")["href"]

    #strips the item URL to get it down to the base webpage URL
    rootUrl = itemUrl.rsplit('/', 2)[0]

    #finds string of current sale price on page
    priceString = soup.find(class_=re.compile("current-sale-price")).text
    #converts price to a numerical value
    itemPrice = float(priceString.replace("$", ""))

def connect():
    return mysql.connector.connect(
        host=mHost,
        user=mUser,
        password=mPassword,
        database=mDatabase
    )


#def pushtoDatabase():


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    scrape()


