import requests
import re
import mysql.connector
from bs4 import BeautifulSoup

#defining mysql variables
mHost = "localhost"
mUser = "root"
mPassword = "root"
mDatabase = "jeans"

def scrape(url):
    #url = "https://oldnavy.gap.com/browse/product.do?pid=846874002&vid=1&pcid=85729&cid=85729&nav=meganav%3AWomen%3AWomen%27s+Bottoms%3AJeans#pdp-page-content"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    brandName = (soup.title.string).split(" | ", 1)[1]
    #stores page title, usually includes item name IN THIS CASE it splits off the brand name
    itemName = (soup.title.string).split(" | ")[0]
    #finds item URL
    itemUrl = soup.find("link", rel="canonical")["href"]

    #extracts PID from canonical link (itemURL)
    itemPID = itemUrl.split("pid=",1)[1]

    #strips the item URL to get it down to the base webpage URL
    rootUrl = itemUrl.rsplit('/', 2)[0]

    #find img source
    imageStem = soup.find("img", alt=lambda x: x and itemName.lower() in x.lower())["src"]

    #combines base URL and img src to create a full link
    itemImg = rootUrl + imageStem

    #finds string of current sale price on page
    priceString = soup.find(class_=re.compile(r"current.*price")).text
    #converts price to a numerical value
    itemPrice = float(priceString.replace("$", ""))

    return brandName, itemName, itemUrl, itemPID, rootUrl, itemImg, itemPrice,

def connect():
    return mysql.connector.connect( host=mHost, user=mUser, password=mPassword, database=mDatabase )

def addItem(brandName, itemName, itemUrl, itemPID, rootUrl, itemImg, itemPrice):
    #VALUES (
    #   p_brandName
    #   p_rootUrl,
    #   p_itemUrl,
    #   p_itemImg,
    #   p_itemPid,
    #   p_itemName,
    #   p_itemPrice
    #);
    conn = connect()
    cursor = conn.cursor()

    cursor.callproc("AddItem", [brandName, rootUrl, itemUrl, itemImg, itemPID, itemName, itemPrice])
    conn.commit()

    print("Item " + itemName + " added.")
    conn.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    continueProgram = 1
    while continueProgram:
        url = input("Paste the full URL of your item: ")
        item = scrape(url)
        addItem(*item)
        userContinue = input("Would you like to add another item? (y/n)")
        if userContinue == "n":
            continueProgram = 0

