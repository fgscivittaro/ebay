import requests, re
from bs4 import BeautifulSoup

#Scrapes the eBay home page and returns a list of links from the home page's
#Featured Collections, and every link within each collection.
url = 'http://www.ebay.com/'
soup = BeautifulSoup(requests.get(url).text, 'html.parser')

no_lazy = soup.find_all('div', attrs = {'class':'no-lazy'})
featured_links = []

#Returns the link of each Featured Collection displayed on the main page.
for html_code in no_lazy:
    featured_links.append(html_code.find('a').get('href'))

product_links = []
final_links = []

#Iterates through the link of each Featured Collection.
for html_url in featured_links:
    html_soup = BeautifulSoup(requests.get(html_url).text, 'html.parser')

    #Generates the URL of an xml ajax request responsible for retrieving some
    #but not all of the product links.
    editor = html_url[24:]
    slash = editor.index('/')
    editor = editor[:slash]
    col_code = html_url[-12:]
    lxml_url = 'http://www.ebay.com/cln/_ajax/2/%s/%s' % (editor, col_code)
    limiter = {'itemsPerPage':'30'}
    lxml_soup = BeautifulSoup((requests.get(lxml_url, params=limiter).content), 'lxml')

    #Iterates through all the URLs found within the HTML code and appends them.
    item_thumb = html_soup.find_all('div', attrs={'class':'itemThumb'})
    for html_code in item_thumb:
        product_links.append(html_code.find('a').get('href'))

    #Retrieves all the URLs that the xml code is responsible for.
    final_links = [a["href"] for a in lxml_soup.select("div.itemThumb div.itemImg.image.lazy-image a[href]")]

    #Merges the lists and turns them into a set, since there is some overlap.
    product_links = list(set(product_links + final_links))
    print str(len(product_links)) + " links scraped"
