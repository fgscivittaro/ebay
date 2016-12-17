from scrape_page import *
from collect_links import *

import schedule

def open_new_file(filename):
    """
    Opens a new data file with a specified title; if the title already exists,
    then the function will overwrite the old file and create a new file with
    column headers.
    """

    with open(filename, "w") as initial_file:
        initial_file.write(
        "Time" + ";" +
        "Item ID" + ";" +
        "Title" + ";" +
        "Condition" + ";" +
        "Trending Price ($)" + ";" +
        "List price ($)" + ";" +
        "Product Discount ($)" + ";" +
        "Product Discount (%)" + ";" +
        "Current Price ($)" + ";" +
        "Shipping Cost ($)" + ";" +
        "Item Location" + ";" +
        "Delivery Date" + ";" +
        "Return Policy" + ";" +
        "Total Ratings" + ";" +
        "Product Rating (0.0-5.0)" + ";" +
        "Username" + ";" +
        "Seller Reviews" + ";" +
        "Seller Feedback (%)" + ";" +
        "Hot Info" + ";" +
        "Users Watching" + ";" +
        "Amount Sold" + ";" +
        "Percent Sold (%)" + ";" +
        "Amount Available" + ";" +
        "Inquiries" + ";" +
        "First Reason" + ";" +
        "Second Reason" + ";" +
        "Third Reason" + ";" +
        "Date" + ";" +
        "URL" + "\n"
        )

    print "New file named %s created" % (filename)


def append_data(filename, product_dict):
    """
    Appends already-scraped data to an already-existing file.
    """

    with open(filename, "a") as datafile:
        datafile.write(
            product_dict['Time'] + ";" +
            product_dict['Item ID'] + ";" +
            product_dict['Title'] + ";" +
            product_dict['Condition'] + ";" +
            product_dict['Trending Price'] + ";" +
            product_dict['List Price'] + ";" +
            product_dict['Product Discount ($)'] + ";" +
            product_dict['Product Discount (%)'] + ";" +
            product_dict['Current Price'] + ";" +
            product_dict['Shipping Cost'] + ";" +
            product_dict['Item Location'] + ";" +
            product_dict['Delivery Date'] + ";" +
            product_dict['Return Policy'] + ";" +
            product_dict['Total Ratings'] + ";" +
            product_dict['Product Rating'] + ";" +
            product_dict['Username'] + ";" +
            product_dict['Seller Reviews'] + ";" +
            product_dict['Seller Feedback'] + ";" +
            product_dict['Hot Info'] + ";" +
            product_dict['Users Watching'] + ";" +
            product_dict['Amount Sold'] + ";" +
            product_dict['Percent Sold'] + ";" +
            product_dict['Amount Available'] + ";" +
            product_dict['Inquiries'] + ";" +
            product_dict['First Reason'] + ";" +
            product_dict['Second Reason'] + ";" +
            product_dict['Third Reason'] + ";" +
            product_dict['Date'] + ";" +
            product_dict['URL'] + "\n"
            )

    print "Data appended"


def scrape_and_append_data(url, filename, num_retries  = 10):
    """
    Scrapes data from a desired eBay product page and appends it to an
    already-existing file.
    """

    product_dict = find_all_product_info(url, num_retries)
    print "Data scraped"
    append_data(filename, product_dict)


def scrape_all_data_from_all_featured_products(filename,
                                               link_list,
                                               num_retries = 10):
    """
    Takes a list of featured eBay product links, scrapes all information for
    each link, and appends it to a file.
    """

    for url in link_list:
        scrape_and_append_data(url, filename, num_retries)

    print "Finished appending data for all links"


def write_new_file_and_scrape_all_data(filename, link_list, num_retries = 10):
    """
    Writes a new file, scrapes data from every product link in a list, and
    appends each product's data to the previously created file.
    """

    open_new_file(filename)
    scrape_all_data_from_all_featured_products(filename, link_list, num_retries)


def dynamically_scrape_data(filename, link_list, interval, num_retries = 10):
    """
    Repeatedly runs the scraper every time the specified interval has passed
    and continuously appends the data to a file.
    """

    def job():
        scrape_all_data_from_all_featured_products(filename,
                                                   link_list,
                                                   num_retries)
    job()
    schedule.every(interval).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(30)

    print "Dynamic scraping finished"


def write_new_file_and_dynamically_scrape_all_data(filename,
                                                   link_list,
                                                   interval,
                                                   num_retries = 10):
    """
    Writes a new file and repeatedly runs the scraper every time the specified
    interval has passed and continuously appends the data to a file.
    """

    open_new_file(filename)
    dynamically_scrape_data(filename, link_list, num_retries, interval)


def clean_links_and_scrape(filename, num_retries = 10):
    """
    Cleans the link list by checking for and removing bad links. Once the bad
    links have been removed, the function scrapes the clean list and appends the
    data to a file.
    """

    link_list = collect_all_featured_links()
    bad_links = collect_bad_links(link_list)
    clean_links = remove_bad_links_from_link_list(bad_links, link_list)

    scrape_all_data_from_all_featured_products(filename,
                                               clean_links,
                                               num_retries)


def clean_links_and_dynamically_scrape(filename, interval, num_retries = 10):
    """
    Repeatedly updates the link list and runs the scraper every time the
    specified interval has passed and continuously appends the data to a file.
    """

    def job():
        clean_links_and_scrape(filename, num_retries)

    job()
    schedule.every(interval).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(30)

    print "Dynamic scraping finished"


def write_new_file_update_links_and_dynamically_scrape(filename,
                                                       interval,
                                                       num_retries = 10):
    """
    Writes a new file and repeatedly updates the link list and runs the scraper
    every time the specified interval has passed and continuously appends the
    data to a file.
    """

    open_new_file(filename)
    clean_links_and_dynamically_scrape(filename, interval, num_retries)
