import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from sale import Sale

import time
import re
from bs4 import BeautifulSoup
from time import localtime


def find_all_product_info(url, num_retries = 10):
    """
    Returns all the information for a product in a dict
    """

    soup = get_soup(url, num_retries)

    date, time = get_date_and_time()
    discount_raw, discount_percent = get_product_discount(soup)
    reason1, reason2, reason3 = get_three_reasons(soup)

    product_dict = {
    'Date': date,
    'Time': time,
    'Item ID': get_item_number(soup),
    'Title': get_title(soup),
    'Product Rating': get_product_rating(soup),
    'Total Ratings': get_total_ratings(soup),
    'Username': get_username(soup),
    'Seller Reviews': get_seller_reviews(soup),
    'Seller Feedback': get_seller_feedback(soup),
    'Hot Info': get_hot_info(soup),
    'Condition': get_condition(soup),
    'Amount Sold': get_amount_sold(soup),
    'Percent Sold': get_percent_sold(soup),
    'First Reason': reason1,
    'Second Reason': reason2,
    'Third Reason': reason3,
    'Amount Available': get_amount_available(soup),
    'Inquiries': get_inquiries(soup),
    'Trending Price': get_trending_price(soup),
    'List Price': get_list_price(soup),
    'Product Discount ($)': discount_raw,
    'Product Discount (%)': discount_percent,
    'Current Price': get_current_price(soup),
    'Shipping Cost': get_shipping_cost(soup),
    'Users Watching': get_users_watching(soup),
    'Item Location': get_item_location(soup),
    'Delivery Date': get_delivery_date(soup),
    'Return Policy': get_return_policy(soup),
    'URL': url
    }

    return product_dict


def get_soup(url, num_retries = 10):
    """
    Takes in a url and returns the parsed BeautifulSoup code for that url with
    handling capabilities if the request 'bounces'.
    """

    s = requests.Session()

    retries = Retry(
        total = num_retries,
        backoff_factor = 0.1,
        status_forcelist = [500, 502, 503, 504]
        )

    s.mount('http://', HTTPAdapter(max_retries = retries))

    return BeautifulSoup(s.get(url).text, 'html.parser')


def get_date_and_time():
    """
    Returns the current date and time as a tuple (date, time)
    """

    mydate = time.strftime("%m/%d/%Y", localtime())
    mytime = time.strftime("%H:%M:%S", localtime())

    return (mydate, mytime)


def get_item_number(soup):
    """
    Returns the product's unique item_number
    """

    item_number = soup.find('div', attrs = {'id':'descItemNumber'})

    if not item_number:
        return "N/A"

    item_number = item_number.get_text()

    return item_number


def get_title(soup):
    """
    Returns the product title. If there is an unknown character in the title, it
    returns it as '?'.
    """

    title = soup.find('h1', attrs = {'class':'it-ttl'})

    if not title:
        return "N/A"

    for i in title('span'):
       i.extract()
    title = title.get_text().encode('ascii','replace')

    return title


def get_product_rating(soup):
    """
    Returns the product's rating, which is an int from 0 to 5 (five stars)
    """

    product_rating = soup.find('span', attrs = {'class':'reviews-seeall-hdn'})

    if not product_rating:
        return "N/A"

    product_rating = product_rating.get_text().replace(u'\xa0', u' ')[:3]

    return product_rating


def get_total_ratings(soup):
    """
    Returns the total number of ratings the product has received
    """

    total_ratings = soup.find('a', attrs = {'class':"prodreview vi-VR-prodRev"})

    if not total_ratings:
        return "0"

    total_ratings = (total_ratings.get_text()
                                 .replace(u',', u'')
                                 .replace(u'product', u'')[:-7]
                                 .strip())

    return total_ratings


def get_username(soup):
    """
    Returns the seller's eBay username
    """

    username = soup.find('span', attrs = {'class':'mbg-nw'})

    if not username:
        return "N/A"

    username = username.get_text().encode('ascii','replace')

    return username


def get_seller_reviews(soup):
    """
    Returns the total number of reviews the seller has received
    """

    seller_reviews = soup.find('span', attrs = {'class':'mbg-l'})

    if not seller_reviews:
        return "N/A"

    seller_reviews = seller_reviews.find('a').get_text()

    return seller_reviews


def get_seller_feedback(soup):
    """
    Returns the seller's positive feedback rating, given as a percent
    """

    seller_feedback = soup.find('div', attrs = {'id':'si-fb'})

    if not seller_feedback:
        return "N/A"

    seller_feedback = (seller_feedback.get_text()
                                      .replace(u'\xa0', u' ')[:-19])

    return seller_feedback


def get_hot_info(soup):
    """
    Returns the information given by eBay next to the "fire" emblem under the
    title. This information is chosen by eBay and varies greatly.
    """

    hot_info = soup.find('div', attrs = {'id':'vi_notification_new'})

    if not hot_info:
        return "N/A"

    hot_info = (hot_info.get_text()
                        .strip()
                        .replace(u',', u'')
                        .encode('ascii','replace'))

    return hot_info


def get_condition(soup):
    """
    Returns the declared condition of the item
    """

    condition = soup.find('div', attrs = {'class':"u-flL condText  "})

    if not condition:
        return "N/A"

    for i in condition('span'):
        condition = i.extract()
    condition = condition.get_text()

    return condition


def get_amount_sold(soup):
    """
    Returns how many units of the product have been sold
    """

    amount_sold = soup.find('span',
    attrs = {'class':["qtyTxt", "vi-bboxrev-dsplblk", "vi-qty-fixAlignment"]})

    if not amount_sold:
        return "N/A"

    amount_sold_link = amount_sold.find('a')

    if not amount_sold_link:
        return "N/A"

    amount_sold = amount_sold_link.get_text().replace(u',', u'')[:-5]

    return amount_sold


def get_percent_sold(soup):
    """
    Returns the percent of inventory sold, if it is made available
    """

    why_to_buy = soup.find('div', attrs = {'id':'why2buy'})

    if not why_to_buy:
        return "N/A"

    # Specifically looks for information following the format:
    # "More than X% sold"
    sold_pattern = re.compile(r'More than')
    percent_sold = why_to_buy.find(text = sold_pattern)

    if not percent_sold:
        return "N/A"

    percent_sold = (percent_sold.replace(u'More than ',u'')
                                .replace(u'% ',u'')
                                .replace(u'sold',u'')
                                .encode('ascii','replace'))

    return percent_sold


def get_three_reasons(soup):
    """
    Takes in the eBay page's soup code and parses it for the (up to) three
    reasons eBay lists for why the buyer should buy.
    """

    why_to_buy = soup.find('div', attrs = {'id':'why2buy'})
    reasons = ["N/A"] * 3

    if why_to_buy:
        all_reasons = why_to_buy.find_all('span', attrs = {'class':'w2b-sgl'})
    else:
        return (reasons[0], reasons[1], reasons[2])

    for i, reason in enumerate(all_reasons):
        clean_reason = reason.get_text().encode('ascii','replace')
        reasons[i] = clean_reason

    return (reasons[0], reasons[1], reasons[2])


def get_amount_available(soup):
    """
    Returns how many available units of the product are left
    """

    amount_available = soup.find('span', attrs = {'id':'qtySubTxt'})

    if not amount_available:
        return "N/A"

    amount_available = amount_available.get_text().strip()
    if amount_available == "More than 10 available":
        return ">10"
    elif amount_available == "Limited quantity available":
        return "Limited quantity"
    elif amount_available == "Last one":
        return "1"
    else:
        return amount_available[:-10]


def get_inquiries(soup):
    """
    Returns the number of inquiries, if the information is displayed
    """

    pattern = re.compile(r'inquiries')
    inquiries = soup.find(text = pattern)

    if not inquiries:
        return "N/A"

    inquiries = inquiries.replace(u',', u'')[:-10]

    return inquiries


def get_trending_price(soup):
    """
    Returns the trending price of the product
    """

    trending_price = soup.find('div',
                                attrs = {'class':'u-flL vi-bbox-posTop2 '})

    if not trending_price:
        return "N/A"

    for i in trending_price('div'):
        i.extract()
    trending_price = (trending_price.get_text()
                                    .strip()
                                    .replace(u',', u'')
                                    .encode('ascii','replace'))
    if trending_price[0] == "$":
        trending_price = trending_price.replace(u'$',u'').strip()
    elif trending_price[:2] == "US":
        trending_price = (trending_price.replace(u'US ', u'')
                                        .replace(u'$',u'')
                                        .strip())
    elif (trending_price[:3] == "GBP"
    or trending_price[1] == "C"
    or trending_price[:2] == "AU"
    or trending_price[:3] == "EUR"):
        trending_price = "Foreign currency"
    else:
        trending_price = "Unknown currency"

    return trending_price


def get_list_price(soup):
    """
    Returns the original price of the product
    """

    list_price = soup.find('span', attrs = {'id':['orgPrc', 'mm-saleOrgPrc']})

    if not list_price:
        return "N/A"

    list_price = (list_price.get_text()
                            .strip()
                            .replace(u'US ', u'')
                            .replace(u'$', u'')
                            .replace(u',', u'')
                            .encode('ascii','replace'))
    if list_price == "":
        list_price = "N/A"
    elif (list_price[:3] == "GBP"
    or list_price[1] == "C"
    or list_price[:2] == "AU"
    or list_price[:3] == "EUR"):
        list_price = 'Foreign currency'
    else:
        list_price = list_price.strip()

    return list_price


def get_product_discount(soup):
    """
    Returns the product discount as a tuple (raw amount, percent amount)
    """

    you_save = soup.find('span', attrs = {'id':'youSaveSTP'})

    if not you_save:
        you_save = soup.find('div', attrs = {'id':'mm-saleAmtSavedPrc'})

    if you_save:
        you_save = (you_save.get_text()
                            .strip()
                            .replace(u'\xa0', u' ')
                            .replace(u'US ', u'')
                            .replace(u',', u''))

        if you_save == "(% off)":
            you_save_raw = "N/A"
            you_save_percent = "N/A"

        elif (you_save[:3] == "GBP"
        or you_save[1] == "C"
        or you_save[:2] == "AU"
        or you_save[:3] == "EUR"):
            you_save_raw = "N/A"
            you_save_percent = "N/A"

        else:
            you_save_raw = you_save[1:-9].strip().encode('ascii','replace')
            you_save_percent = (you_save.replace(you_save_raw, u'')
                                        .replace(u'$',u'')
                                        .replace(u'(',u'')
                                        .replace(u'% off)',u'')
                                        .strip()
                                        .encode('ascii','replace'))
    else:
        you_save_raw = "N/A"
        you_save_percent = "N/A"

    return (you_save_raw, you_save_percent)


def get_current_price(soup):
    """
    Returns the product's current price, after discounts
    """

    now_price = soup.find('span', attrs = {'id':'prcIsum'})

    if not now_price:
        now_price = soup.find('span', attrs = {'id':'mm-saleDscPrc'})

    if not now_price:
        return "N/A"

    now_price = (now_price.get_text()
                          .replace(u',', u'')
                          .encode('ascii','replace'))

    if now_price[:2] == "US":
        now_price = now_price[4:].encode('ascii','replace')

    elif (now_price[:3] == "GBP"
    or now_price[1] == "C"
    or now_price[:2] == "AU"
    or now_price[:3] == "EUR"):

        now_price = soup.find('span', attrs = {'id':'convbinPrice'})
        if now_price:
            for i in now_price('span'):
                i.extract()
            now_price = now_price.get_text()[4:].encode('ascii','replace')
        else:
            now_price = soup.find('span', attrs={'id':'convbidPrice'})
            for i in now_price('span'):
                i.extract()
            now_price = now_price.get_text()[4:].encode('ascii','replace')

    else:
        now_price = "Unknown currency"

    return now_price


def get_shipping_cost(soup):
    """
    Returns the product's shipping costs
    """

    shipping_cost = soup.find('span', attrs = {'id':'fshippingCost'})

    if shipping_cost:
        shipping_cost = (shipping_cost.get_text()
                                      .replace(u',', u'')
                                      .strip()
                                      .encode('ascii','replace'))
        if (shipping_cost[:3] == "GBP"
        or shipping_cost[1] == "C"
        or shipping_cost[:2] == "AU"
        or shipping_cost[:3] == "EUR"):
            shipping_cost = soup.find('span', attrs = {'id':'convetedPriceId'})
            shipping_cost = shipping_cost.get_text()[4:]
        elif shipping_cost == "FREE":
            shipping_cost = "0.00"
        elif shipping_cost[0] == "$":
            shipping_cost = shipping_cost.replace(u'$',u'')
        else:
            shipping_cost = "Unknown currency"
    else:
        """
        Sometimes the shipping cost is not given, and some supplementary
        information such as "Local pickup" is given. In this case, the scraper
        performs a naive search for the first bit of information that seems
        relevant.
        """

        shipping_cost = soup.find('span', attrs = {'id':'shSummary'})
        if shipping_cost:
            shipping = []
            for i in shipping_cost('span'):
                shipping.append(i.extract())
            for i in shipping:
                shipping_cost = i.get_text().strip().encode('ascii','replace')
                if shipping_cost != "" and shipping_cost != "|":
                    break
        else:
            shipping_cost = "N/A"

    return shipping_cost


def get_users_watching(soup):
    """
    Returns the total number of users watching the product
    """

    total_watching = soup.find('span', attrs = {'class':'vi-buybox-watchcount'})

    if not total_watching:
        return "N/A"

    total_watching = total_watching.get_text().replace(u',', u'')

    return total_watching


def get_item_location(soup):
    """
    Returns the seller's location--where the item will be shipped from
    """

    item_location = soup.find('div', attrs = {'class':'iti-eu-bld-gry'})

    if not item_location:
        return "N/A"

    item_location = (item_location.get_text()
                                  .strip()
                                  .encode('ascii','replace'))

    return item_location


def get_delivery_date(soup):
    """
    Returns the estimated date at which the product will be delivered to the
    location of the computer that makes the page request.
    """

    delivery_date = soup.find('span', attrs = {'class':'vi-acc-del-range'})

    if not delivery_date:
        return "N/A"

    delivery_date = (delivery_date.get_text()
                                  .replace(u'and', u'-')
                                  .encode('ascii','replace'))

    return delivery_date


def get_return_policy(soup):
    """
    Returns the return policy offered by the seller
    """

    return_policy = soup.find('span', attrs = {'id':'vi-ret-accrd-txt'})

    if not return_policy:
        return "N/A"

    return_policy = (return_policy.get_text()
                                  .replace(u'\xa0', u' ')
                                  .strip()
                                  .encode('ascii','replace'))
    if len(return_policy) > 79:
        # Done for aesthetic reasons, in case the description is wordy
        return_policy = return_policy[:79] + "..."

    return return_policy


def get_sales_history(soup):
    """
    Returns a dictionary containing the history of the product's sales (up to
    the 100 most recent sales) in which a counter is assigned as the key
    mapping to the sale information.
    """

    amount_sold = soup.find('span',
    attrs = {'class':["qtyTxt", "vi-bboxrev-dsplblk", "vi-qty-fixAlignment"]})

    if not amount_sold:
        return {}

    sales_dict = {}

    history_link = amount_sold.find('a').get('href')
    new_soup = get_soup(history_link)
    sales_list = new_soup.find_all('tr',
                                   attrs = {'bgcolor':['#ffffff', '#f2f2f2']})

    for i in range(len(sales_list)):
        color = (sales_list[i].find('td', attrs = {
                                     'class':'variationContentValueFont'}))

        if color:
            color = color.get_text().replace(u'Color: ',u'')
        else:
            color = "N/A"

        other_info = sales_list[i].find_all('td', attrs={
                                            'class':'contentValueFont'})

        price = other_info[0].get_text().replace(u'US $',u'')
        quantity = other_info[1].get_text()
        datetime = other_info[2].get_text()

        sales_dict[i + 1] = Sale(datetime, price, quantity, color)

    return sales_dict
