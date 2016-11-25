from ebay_scraper import *
from ebay_links import *

def scrape_all_info_from_all_featured_products(num_retries = 10):
    """
    Takes a list of featured eBay product links, scrapes all information for
    each link, and appends it to a file.
    """

    for url in collect_all_featured_links():
        find_all_product_info(url, num_retries = 10)
