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


#these functions as list for each type of content i record
prices = []
names = []
availabilities =[]
stars = []
links = []

book_list.pop(-1)
book_list.pop(-1)
for book in book_list:
    #instancing the variables
    bprice = book.find('p', class_='price_color')
    binstock = book.find('p', class_='instock')
            #find all a tags
    bname = book.find_all('a')
    bstars = book.find('p', class_='star-rating')

    #appending elements
        #get text basicalyljust gets the text inside the tag
    prices.append(bprice.get_text())
        # so attrs.get(value) sometimes you need to [index] 
        # but attrs.get(value) is to return the contents of the tag attributes into a string
    names.append(bname[1].attrs.get('title'))
    stars.append(bstars.attrs.get('class')[1])
    links.append(bname[1].attrs.get('href'))
    #sometimes values are as simple as true and false state ments, 
    # and in those times you can do some thing like this, cheking for a substring to detect, 
    # and if the substring is there certain prgrams of your choosing will run
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

