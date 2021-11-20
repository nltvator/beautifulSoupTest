import requests
from bs4 import BeautifulSoup
import pandas as pd

page = requests.get("http://books.toscrape.com")

soup = BeautifulSoup(page.content, 'html.parser')

df = pd.DataFrame(columns=['Book Title', 'Price'])

#print(soup.prettify())

found = False

while not found:

    nextPage = soup.find("li", {"class":"next"})
    try:
        nextPageLink = nextPage.find(href=True)
    except:
        found = True

    products = soup.find("ol", {"class":"row"})

    productPods = products.find_all("li", {"class":"col-xs-6 col-sm-4 col-md-3 col-lg-3"})

    for book in productPods:
        bookLink = book.find("h3")
        bookTitle = bookLink.find("a").getText()
        bookLinkPrice = book.find("div", {"class":"product_price"})
        bookPrice = bookLinkPrice.find("p", {"class":"price_color"}).getText()
        df = df.append({"Book Title": bookTitle, "Price": bookPrice}, ignore_index=True)
    
    hrefNextPage = "http://books.toscrape.com/" + nextPageLink['href']

    if "catalogue" not in hrefNextPage:
        hrefNextPage = "http://books.toscrape.com/catalogue/" + nextPageLink['href']

    page = requests.get(hrefNextPage)
    soup = BeautifulSoup(page.content, 'html.parser')

df.to_csv("ScrapedBooksBS4.csv")