from collect_data import *
from collect_sales_data import *

import schedule

def write_new_files(data_filename, sales_filename):
    """
    Writes two new files, one for product data, the other for product sales
    history.
    """

    open_new_file(data_filename)
    open_new_sales_file(sales_filename)


def scrape_and_append_combined_data(url,
                                    data_filename,
                                    sales_filename,
                                    num_retries = 10):
    """
    Scrapes all data from a product page and appends it to the two files.
    """

    scrape_and_append_data(url, data_filename, num_retries)
    scrape_and_append_sales_data(url, sales_filename, num_retries)


def scrape_combined_data_from_all_featured_products(data_filename,
                                                    sales_filename,
                                                    link_list,
                                                    num_retries = 10):
    """
    Scrapes all data from every featured product and appends that data to
    their respective files.
    """

    for url in link_list:
        scrape_and_append_combined_data(url,
                                        data_filename,
                                        sales_filename,
                                        num_retries)


def clean_links_and_scrape_combined_data(data_filename,
                                         sales_filename,
                                         num_retries = 10):
    """
    Scrapes a list of clean featured links and appends the data to their
    respective files.
    """

    link_list = collect_all_featured_links()
    bad_links = collect_bad_links(link_list)
    clean_links = remove_bad_links_from_link_list(bad_links, link_list)

    scrape_combined_data_from_all_featured_products(data_filename,
                                                    sales_filename,
                                                    clean_links,
                                                    num_retries)


def dynamically_scrape_combined_data(data_filename,
                                     sales_filename,
                                     interval,
                                     num_retries = 10):
    """
    Dynamically scrapes a continuously updated list of unique clean links and
    appends the data to their respective files.
    """

    old_list = []

    def job(old_list):
        new_list = collect_all_featured_links()
        new_links = remove_old_links(old_list, new_list)
        bad_links = collect_bad_links(new_links)
        clean_links = remove_bad_links_from_link_list(bad_links, new_links)

        scrape_combined_data_from_all_featured_products(data_filename,
                                                        sales_filename,
                                                        clean_links,
                                                        num_retries)

        old_list = new_list

    job(old_list)
    schedule.every(interval).hours.do(job)

    while True:
        schedule.run_pending()
        time.sleep(30)

    print "Dynamic scraping finished"


def write_new_files_and_dynamically_scrape_combined_data(data_filename,
                                                         sales_filename,
                                                         interval,
                                                         num_retries = 10):
    """
    Writes a new file and then dynamically scrapes sales data.
    """

    write_new_files(data_filename, sales_filename)
    dynamically_scrape_combined_data(data_filename,
                                     sales_filename,
                                     interval,
                                     num_retries)
