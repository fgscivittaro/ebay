import requests
from bs4 import BeautifulSoup

#Scrapes the eBay home page and returns a list of links.
url = 'http://www.ebay.com/'
soup = BeautifulSoup(requests.get(url).text, 'html.parser')

no_lazy = soup.find_all('div', attrs = {'class':'no-lazy'})
link_list = []

for link in no_lazy:
    link_list.append(link.find('a').get('href'))

product_list = []

for link in link_list:
    soup = BeautifulSoup(requests.get(link).text, 'html.parser')
    #For some reason, this does not return every single item.
    item_thumb = soup.find_all('div', attrs={'class':'itemThumb'})
    for link in item_thumb:
        product_list.append(link.find('a').get('href'))

print product_list
