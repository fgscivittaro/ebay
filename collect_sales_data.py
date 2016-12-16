from scrape_page import *
from collect_links import *

def open_new_sales(filename):
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
    sales_dict = get_sold_history(soup)

    if sales_dict:
        item_id = get_item_number(soup)
        with open(filename, "a") as data_file:
            data_file.write(
            item_id + ';' +
            sales_dict['UserID'] + ';' +
            sales_dict['Date and Time'] + ';' +
            sales_dict['Price ($)'] + ';' +
            sales_dict['Quantity'] + ';' +
            sales_dict['Color'] + '\n'
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

    open_new_sales(filename)
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
    Dynamically scrapes sales data and appends the data to a file.
    """

    def job():
        # What?

    schedule.every(interval).hours.do(job)

    while True:
        schedule.run_pending()
        time.sleep(30)

    print "Dynamic scraping finished"
