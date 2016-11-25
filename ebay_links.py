import requests
import re
from bs4 import BeautifulSoup

from ebay_scraper import get_soup

def collect_featured_links():
    """
    Scrapes the eBay home page and returns the links to each featured collection

    Inputs: none

    Returns: a list of links, each of which corresponds to an eBay featured
        collection
    """

    soup = get_soup('http://www.ebay.com/')
    no_lazy = soup.find_all('div', attrs = {'class':'no-lazy'})
    featured_links = []

    # Returns the link of each Featured Collection displayed on the main page.
    for html_code in no_lazy:
        featured_links.append(html_code.find('a').get('href'))

    return featured_links


def collect_featured_products(url):
    """
    Takes in the url of a featured collection and returns all the product links
    within the collection

    Inputs:
        url: the url of a featured collection

    Returns: a list of the product links found within the featured collection
    """

    soup = get_soup(url)
    product_links = []

    # Iterates through all the URLs found within the HTML code and appends them
    # to product_links
    item_thumb = soup.find_all('div', attrs={'class':'itemThumb'})
    for html_code in item_thumb:
        product_links.append(html_code.find('a').get('href'))

    # Generates the URL of an xml ajax request responsible for retrieving some
    # but not all of the product links
    editor = url[24:]
    slash = editor.index('/')
    editor = editor[:slash]
    col_code = url[-12:]
    lxml_url = 'http://www.ebay.com/cln/_ajax/2/%s/%s' % (editor, col_code)
    limiter = {'itemsPerPage':'30'}
    lxml_soup = BeautifulSoup((requests.get(
                               lxml_url,
                               params = limiter).content),
                               'lxml')

    # Retrieves all the URLs that the xml code is responsible for
    lxml_links = [a["href"] for a in lxml_soup.select(
    "div.itemThumb div.itemImg.image.lazy-image a[href]")]

    # Merges the lists and turns them into a set, since there is some overlap
    # between the two
    all_links = list(set(product_links + lxml_links))

    return all_links


def collect_all_featured_links():
    """
    Iterates through collect_featured_links and returns a combined list of all
    the featured product links within all of the featured collections.

    Inputs: none

    Returns: A list of every featured url found in all the featured collections
    on eBay's home page
    """

    all_links = []

    for url in collect_featured_links():
        all_links += collect_featured_products(url)

    return all_links
