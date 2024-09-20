from bs4 import BeautifulSoup
import requests
import re
import pandas as pd


headers = {'Accept-Language': 'en-US,en;q=0.8'}
url ='https://books.toscrape.com'
response = requests.get(url,headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

bg = soup.select('section')
book_list = bg[0].find_all('li')



prices = []
names = []
availabilities =[]
stars = []
links = []

book_list.pop(-1)
book_list.pop(-1)
for book in book_list:
    bprice = book.find('p', class_='price_color')
    binstock = book.find('p', class_='instock')
    bname = book.find_all('a')
    bstars = book.find('p', class_='star-rating')
    prices.append(bprice.get_text())
    names.append(bname[1].attrs.get('title'))
    stars.append(bstars.attrs.get('class')[1])
    links.append(bname[1].attrs.get('href'))
    if "In stock"in binstock.get_text():
        availabilities.append("instock")
    else:
        availabilities.append("not instock")


df = pd.DataFrame(
    {'book title': names,
     'link': links,
     'availability': availabilities,
     'price': prices,
     'star rating': stars
     }
    )

print (df.head())

df.to_csv('book_scrape.csv', index=False)

