from scrape_page import *
from collect_links import *

import schedule

def open_new_sales_file(filename):
        """
        Opens a new sales data file with a specified title; if the title already exists,
        then the function will overwrite the old file and create a new file with
        column headers.
        """

        with open(filename, "w") as initial_file:
            initial_file.write(
            'Item ID' + ';' +
            'UserID' + ';' +
            'Date and Time' + ';' +
            'Price ($)' + ';' +
            'Quantity' + ';' +
            'Color' + '\n'
            )

        print "New file named %s created" % (filename)


def scrape_and_append_sales_data(url, filename, num_retries = 10):
    """
    Scrapes desired information from the product page and appends it to an
    already-existing file.
    """

    soup = get_soup(url, num_retries = 10)
    sales_dict = get_sales_history(soup)

    if sales_dict:
        item_id = get_item_number(soup)
        for key in sales_dict:
            with open(filename, "a") as data_file:
                data_file.write(
                item_id + ';' +
                sales_dict[key].transaction_id + ';' +
                sales_dict[key].datetime + ';' +
                sales_dict[key].price + ';' +
                sales_dict[key].quantity + ';' +
                sales_dict[key].color + '\n'
                )

    print "Data scraped and appended"


def scrape_and_append_sales_data_from_featured_links(filename,
                                                     link_list,
                                                     num_retries = 10):
    """
    Scrapes sales data from a list of links and appends it to a file.
    """

    for url in link_list:
        scrape_and_append_sales_data(url, filename, num_retries)

    print "Finished scraping sales data from all links"


def write_new_file_and_scrape_all_sales_data(filename,
                                             link_list,
                                             num_retries = 10):
    """
    Writes a new file and scrape the sales data from every product in the
    link list.
    """

    open_new_sales_file(filename)
    scrape_and_append_sales_data_from_featured_links(filename,
                                                     link_list,
                                                     num_retries)


def clean_links_and_scrape_sales_data(filename, num_retries = 10):
    """
    Cleans the link list by checking for and removing bad links. Once the bad
    links have been removed, the function scrapes the clean list and appends the
    data to a file.
    """

    link_list = collect_all_featured_links()
    bad_links = collect_bad_links(link_list)
    clean_links = remove_bad_links_from_link_list(bad_links, link_list)

    scrape_and_append_sales_data_from_featured_links(filename,
                                                     clean_links,
                                                     num_retries)


def dynamically_scrape_and_append_sales_data(filename,
                                             interval,
                                             num_retries = 10):
    """
    Dynamically scrapes sales data and appends the data to a file by generating
    a list of links, checking it against an old list and only keeping new links,
    and scraping those links for sales data.
    """

    old_list = []

    def job(old_list):
        new_list = collect_all_featured_links()
        new_links = remove_old_links(old_list, new_list)
        bad_links = collect_bad_links(new_links)
        clean_links = remove_bad_links_from_link_list(bad_links, new_links)

        scrape_and_append_sales_data_from_featured_links(filename,
                                                         clean_links,
                                                         num_retries)

        old_list = new_list

    job(old_list)
    schedule.every(interval).hours.do(job)

    while True:
        schedule.run_pending()
        time.sleep(30)

    print "Dynamic scraping finished"


def write_new_file_and_dynamically_scrape_all_sales_data(filename,
                                                         interval,
                                                         num_retries):
    """
    Writes a new file and then dynamically scrapes sales data.
    """

    open_new_sales_file(filename)
    dynamically_scrape_and_append_sales_data(filename,
                                             interval,
                                             num_retries)
