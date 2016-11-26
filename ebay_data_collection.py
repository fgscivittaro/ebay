from ebay_scraper import *
from ebay_links import *

def open_new_file(filename):
    """
    Opens a new data file with a specified title; if the title already exists,
    then the function will overwrite the old file and create a new file with
    column headers.

    Inputs: (a string) the title of the new file; must be a .txt file

    Returns: N/A - writes a new file
    """

    with open(filename, "w") as initial_file:
        initial_file.write(
        "Time;Item ID;Title;Condition;Trending Price ($);List price ($);" +
        "Product Discount ($);Product Discount (%);Current Price ($);Shipping Cost ($);" +
        "Item Location;Delivery Date;Return Policy;Total Ratings;" +
        "Product Rating (0.0-5.0);Username;Seller Reviews;Seller Feedback (%);" +
        "Hot Info;Users Watching;Amount Sold;Percent Sold (%);Amount Available;Inquiries;" +
        "First Reason;Second Reason;Third Reason;Date;URL" + "\n"
        )

    print "New file named %s created" % (filename)


def append_data(filename, product_dict):
    """
    Appends already-scraped data to an already-existing file.

    Inputs:
        filename: the file to append to; must be a .txt file
        product_dict: a dictionary containing the data to append

    Returns:
        N/A - appends to a file
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

    Inputs:
        url: the url of the eBay product page
        filename: the file to append to; must be a .txt file
        num_retries: (default set to 10) the maximum number of retries in the
            case of 'bounces' before a fatal error is triggered

    Returns:
        N/A - appends to a file
    """

    product_dict = find_all_product_info(url, num_retries)
    print "Data scraped"
    append_data(filename, product_dict)


def scrape_all_data_from_all_featured_products(filename, num_retries = 10):
    """
    Takes a list of featured eBay product links, scrapes all information for
    each link, and appends it to a file.

    Inputs:
        filename: the file to append to; must be a .txt file
        num_retries: (default set to 10) the maximum number of retries in the
            case of 'bounces' before a fatal error is triggered.

    Returns:
        N/A - appends to a file
    """

    for url in collect_all_featured_links():
        scrape_and_append_data(url, filename, num_retries)

    print "Finished appending data for all links"


def write_new_file_and_scrape_all_data(filename, num_retries):
    """
    Writes a new file, scrapes data from every product link in a list, and
    appends each product's data to the previously created file.

    Inputs:
        filename: the file to create and append to; must be a .txt file
        num_retries: (default set to 10) the maximum number of retries in the
            case of 'bounces' before a fatal error is triggered.

    Returns:
        N/A - appends to a file
    """

    open_new_file(filename)
    scrape_all_data_from_all_featured_products(filename, num_retries)
