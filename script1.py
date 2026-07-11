import requests
import re
from bs4 import BeautifulSoup

itemName = ''
itemPrice = 0.00

def scrape():
    url = "https://oldnavy.gap.com/browse/product.do?pid=846874002&vid=1&pcid=85729&cid=85729&nav=meganav%3AWomen%3AWomen%27s+Bottoms%3AJeans#pdp-page-content"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    #stores page title, usually includes item name
    itemName = (soup.title.string)

    #finds string of current sale price on page
    priceString = soup.find(class_=re.compile("current-sale-price")).text
    #converts price to a numerical value
    itemPrice = float(priceString.replace("$", ""))



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    scrape()


