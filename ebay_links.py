import requests
from bs4 import BeautifulSoup

#Scrapes the eBay home page and returns a list of links from the home page's Featured Collections.
url = 'http://www.ebay.com/'
soup = BeautifulSoup(requests.get(url).text, 'html.parser')

no_lazy = soup.find_all('div', attrs = {'class':'no-lazy'})
featured_links = []

for link in no_lazy:
    featured_links.append(link.find('a').get('href'))

product_links = []
final_links = []

for html_url in featured_links:
    html_soup = BeautifulSoup(requests.get(html_url).text, 'html.parser')

    editor = html_url[24:]
    slash = editor.index('/')
    editor = editor[:slash]
    col_code = html_url[-12:]

    lxml_url = 'http://www.ebay.com/cln/_ajax/2/%s/%s' % (editor, col_code)
    params = {'itemsPerPage':'30'}
    lxml_soup = BeautifulSoup((requests.get(lxml_url, params=params).content), 'lxml')

    item_thumb = html_soup.find_all('div', attrs={'class':'itemThumb'})
    for link in item_thumb:
        product_links.append(link.find('a').get('href'))

    final_links = [a["href"] for a in lxml_soup.select("div.itemThumb div.itemImg.image.lazy-image a[href]")]

    product_links = list(set(product_links + final_links))
    print len(product_links)
