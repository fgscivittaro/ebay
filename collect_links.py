import requests
import re
from bs4 import BeautifulSoup

from scrape_page import get_soup
from scrape_page import get_title

def collect_featured_links():
    """
    Scrapes the eBay home page and returns the links to each featured collection
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
    within the collection.
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

    print str(len(all_links)) + " links added"
    return all_links


def collect_all_featured_links():
    """
    Iterates through collect_featured_links and returns a combined list of all
    the featured product links within all of the featured collections.
    """

    all_links = []

    for url in collect_featured_links():
        all_links += collect_featured_products(url)

    print "Added all featured links to list"
    return all_links


def collect_bad_links(link_list):
    """
    Some links are for listings that have already ended. These trigger fatal
    errors when BeautifulSoup attempts to scrape them, so they must be removed.
    This function checks for keywords common in bad links and adds the bad links
    to a set.
    """

    bad_links = set([])

    ended1 = re.compile(r'This listing has ended')
    ended2 = re.compile(r'This listing was ended')
    ended3 = re.compile(r'Bidding has ended')

    for link in link_list:
        print "Checking link"
        soup = get_soup(link)
        ended_listing1 = soup.find(text=ended1)
        ended_listing2 = soup.find(text=ended2)
        ended_listing3 = soup.find(text=ended3)
        title = get_title(soup)

        if (ended_listing1
        or ended_listing2
        or ended_listing3
        or title=="N/A"):
            bad_links.add(link)
            print "Bad link added"

    return bad_links


def remove_bad_links_from_link_list(bad_links, link_list):
    """
    Checks the link list for bad links and removes them
    """

    clean_list = []

    for link in link_list:
        if link not in bad_links:
            clean_list.append(link)

    return clean_list


def remove_old_links(old_list, new_list):
    """
    Checks two link lists and returns a list containing links that are in the
    new list but not the old list.
    """

    new_links = []
    old_set = set(old_list)

    for link in new_list:
        if link not in old_set:
            new_links.append(link)

    return new_links
