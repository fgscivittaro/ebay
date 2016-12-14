from scrape_page import *

def open_new_sales(filename):
        """
        Opens a new sales data file with a specified title; if the title already exists,
        then the function will overwrite the old file and create a new file with
        column headers.
        """

        with open(filename, "w") as initial_file:
            initial_file.write(
            'UserID' + ';' +
            'Date and Time' + ';' +
            'Price ($)' + ';' +
            'Quantity' + ';' +
            'Color' + '\n'
            )

        print "New file named %s created" % (filename)


def append_sales_data(filename, sales_dict):
        """
        Appends already-scraped sales data to an already-existing file.
        """

        with open(filename, "a") as datafile:
            datafile.write(
                sales_dict['UserID'] + ";" +
                sales_dict['Date and Time'] + ";" +
                sales_dict['Price ($)'] + ";" +
                sales_dict['Quantity'] + ";" +
                sales_dict['Color'] + "\n"
                )

        print "Sales data appended"
