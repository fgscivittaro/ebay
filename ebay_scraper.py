import requests
import time
import re
from bs4 import BeautifulSoup
from time import localtime

def get_soup(url):
    # Enters the url into BeautifulSoup ad returns the parsed HTML code
    
    s = requests.Session()
    
    """
    Acts as protection against instances in which the request 'bounces' by
    retrying up to ten times before triggering a fatal error.
    """
    
    retries = Retry(
        total=10,
        backoff_factor = 0.1,
        status_forcelist=[ 500, 502, 503, 504 ]
        )

    s.mount('http://', HTTPAdapter(max_retries=retries))

    return BeautifulSoup(s.get(url).text, 'html.parser')


def item_number(soup):
    # Returns the product's unique item_number
    
    item_number = soup.find('div', attrs={'id':'descItemNumber'})
    
    if item_number:
        item_number = item_number.get_text()
    else:
        item_number = "N/A"

    return item_number


def title(soup):
    # Returns the product title. If there is an unknown character in the title, it returns it as '?'.
    
    title = soup.find('h1', attrs={'class':'it-ttl'})
    
    if title:
        for i in title('span'):
           i.extract()
        title = title.get_text().encode('ascii','replace')
    else:
        title = "N/A"

    return title


def product_rating(soup):
    # Returns the product's rating, which is an int from 0 to 5 (five stars)
    
    product_rating = soup.find('span', attrs={'class':'reviews-seeall-hdn'})
    
    if product_rating:
       product_rating = product_rating.get_text().replace(u'\xa0', u' ')[:3]
    else:
       product_rating = 'N/A'
    
    return product_rating


def total_ratings(soup):
    # Returns the total number of ratings the product has received
    
    total_ratings = soup.find('a', attrs={'class':"prodreview vi-VR-prodRev"})
    
    if total_ratings:
       total_ratings = total_ratings.get_text().replace(u',', u'').replace(u'product', u'')[:-7].strip()
    else:
       total_ratings = '0'

    return total_ratings


def username(soup):
    # Returns the seller's eBay username
    
    username = soup.find('span', attrs={'class':'mbg-nw'})
    
    if username:
       username = seller_name.get_text()
    else:
       username = 'N/A'

    return username


def seller_reviews(soup):
    # Returns the total number of reviews the seller has received

    seller_reviews = soup.find('span', attrs={'class':'mbg-l'})
    
    if seller_reviews:
       seller_reviews = seller_reviews.find('a').get_text()
    else:
       seller_reviews = "N/A"

    return seller_reviews


def seller_feedback(soup):
    # Returns the seller's positive feedback rating, given as a percent
    
    seller_feedback = soup.find('div', attrs={'id':'si-fb'})
    
    if seller_feedback:
       seller_feedback = seller_feedback.get_text().replace(u'\xa0', u' ')[:-19]
    else:
       seller_feedback = "N/A"

    return seller_feedback


def hot_info(soup):
    # Returns the information given by eBay next to the "fire" emblem under the title.
    # This information is chosen by eBay and varies greatly
    
    hot_info = soup.find('div', attrs={'id':'vi_notification_new'})
    
    if hot_info:
       hot_info = hot_info.get_text().strip().replace(u',', u'')
    else:
       hot_info = "N/A"

    return hot_info


def condition(soup):
    # Returns the declared condition of the item
    
    condition = soup.find('div', attrs={'class':"u-flL condText  "})
    
    if condition:
        for i in condition('span'):
            condition = i.extract()
        condition = condition.get_text()
    else:
       condition = "N/A"

    return condition


def amount_sold(soup):
    # Returns how many units of the product have been sold
    
    amount_sold = soup.find('span', attrs={'class':["qtyTxt", "vi-bboxrev-dsplblk", "vi-qty-fixAlignment"]})
    
    if amount_sold:
       amount_sold_link = amount_sold.find('a')
       if amount_sold_link:
           amount_sold = amount_sold_link.get_text().replace(u',', u'')[:-5]
       else:
           amount_sold = "N/A"
    else:
       amount_sold = "N/A"

    return amount_sold


def amount_available(soup):
    # Returns how many available units of the product are left
    
    amount_available = soup.find('span', attrs={'id':'qtySubTxt'})
    
    if amount_available:
       amount_available = amount_available.get_text().strip()
       if amount_available=="More than 10 available":
          return ">10"
       elif amount_available=="Limited quantity available":
          return "Limited quantity"
       elif amount_available=="Last one":
          return "1"
       else:
          return amount_available[:-10]
    else:
       return "N/A"


def inquiries(soup):
    # Returns the number of inquiries, if the information is displayed
    
    pattern = re.compile(r'inquiries')
    inquiries = soup.find(text=pattern)
    
    if inquiries:
       inquiries = inquiries.replace(u',', u'')[:-10]
    else:
       inquiries = "N/A"

    return inquiries


def trending_price(soup):
    # Returns the trending price of the product
    
    trending_price = soup.find('div', attrs={'class':'u-flL vi-bbox-posTop2 '})
    
    if trending_price:
       for i in trending_price('div'):
           i.extract()
       trending_price = trending_price.get_text().strip().replace(u',', u'').replace(u'US ', u'')[1:]
    else:
       trending_price = "N/A"

    return trending_price


def list_price(soup):
    # Returns the original price of the product
    
    list_price = soup.find('span', attrs={'id':['orgPrc', 'mm-saleOrgPrc']})
    
    if list_price:
       list_price = list_price.get_text().strip().replace(u'US ', u'').replace(u',', u'')
       if list_price[:3]=="GBP" or list_price[1]=="C" or list_price[:2]=="AU":
           list_price = 'N/A'
       else:
           list_price = list_price.strip()
    else:
       list_price = "N/A"

    return list_price


def product_discount(soup):
    # Returns the product discount as a tuple (raw amount, percent amount)
    
    you_save = soup.find('span', attrs={'id':'youSaveSTP'})
    
    if not you_save:
       you_save = soup.find('div', attrs={'id':'mm-saleAmtSavedPrc'})

    if you_save:
       you_save = you_save.get_text().strip().replace(u'\xa0', u' ').replace(u'US ', u'').replace(u',', u'')
       if you_save[:3]=="GBP" or you_save[1]=="C" or you_save[:2]=="AU":
           you_save_raw = "N/A"
           you_save_percent = "N/A"
       else:
           you_save_raw = you_save[1:-9].strip()
           you_save_percent = you_save.replace(you_save_raw, u'').replace(u'$',u'').replace(u'(',u'').replace(u'% off)',u'').strip()
    else:
       you_save_raw = "N/A"
       you_save_percent = "N/A"

    return (you_save_raw, you_save_percent)


def current_price(soup):
    # Returns the product's current price, after discounts
    
    now_price = soup.find('span', attrs={'id':'prcIsum'})
    
    if not now_price:
       now_price = soup.find('span', attrs={'id':'mm-saleDscPrc'})

    if now_price:
       now_price = now_price.get_text().replace(u',', u'')
    
       if now_price[:3]=="GBP":
           now_price = soup.find('span', attrs={'id':'convbinPrice'})
           if now_price:
               for i in now_price('span'):
                  i.extract()
               now_price = now_price.get_text()[4:]
           else:
               now_price = soup.find('span', attrs={'id':'convbidPrice'})
               for i in now_price('span'):
                  i.extract()
               now_price = now_price.get_text()[4:]
            
            return now_price
            
       elif now_price[1]=="C":
           now_price = soup.find('span', attrs={'id':'convbinPrice'})
           if now_price:
               for i in now_price('span'):
                  i.extract()
               now_price = now_price.get_text()[4:]
           else:
               now_price = soup.find('span', attrs={'id':'convbidPrice'})
               for i in now_price('span'):
                  i.extract()
               now_price = now_price.get_text()[4:]
            
            return now_price
            
       elif now_price[:2]=="AU":
           now_price = soup.find('span', attrs={'id':'convbinPrice'})
           if now_price:
               for i in now_price('span'):
                  i.extract()
               now_price = now_price.get_text()[4:]
           else:
               now_price = soup.find('span', attrs={'id':'convbidPrice'})
               for i in now_price('span'):
                  i.extract()
               now_price = now_price.get_text()[4:]
            
            return now_price
            
       else:
           return now_price[4:]
        
    else:
       return "N/A"


def shipping_cost(soup):
    # Returns the product's shipping costs
    
    shipping_cost = soup.find('span', attrs={'id':'fshippingCost'})
    
    if shipping_cost:
        shipping_cost = shipping_cost.get_text().replace(u',', u'').replace(u'$', u'').strip()
        
        if shipping_cost[:3]=="GBP":
            shipping_cost = soup.find('span', attrs={'id':'convetedPriceId'})
            return shipping_cost.get_text()[4:]
        
        elif shipping_cost[1]=="C":
            shipping_cost = soup.find('span', attrs={'id':'convetedPriceId'})
            return shipping_cost.get_text()[4:]
        
        elif shipping_cost[:2]=="AU":
            shipping_cost = soup.find('span', attrs={'id':'convetedPriceId'})
            return shipping_cost.get_text()[4:]
        
        else:
            if shipping_cost=="FREE":
               return "0.00"

    else:
        shipping_cost = soup.find('span', attrs={'id':'shSummary'})
        if shipping_cost:
            shipping = []
            for i in shipping_cost('span'):
                shipping.append(i.extract())
            for i in shipping:
                shipping_cost = i.get_text().strip()
                if shipping_cost != "" and shipping_cost != "|":
                    return shipping_cost
        else:
            return "N/A"

        
def users_watching(soup):
    # Returns the total number of users watching the product
    
    total_watching = soup.find('span', attrs={'class':'vi-buybox-watchcount'})
    
    if total_watching:
       total_watching = total_watching.get_text().replace(u',', u'')
    else:
       total_watching = "N/A"

    return total_watching


def item_location(soup):
    # Returns the seller's location--where the item will be shipped from
    
    item_location = soup.find('div', attrs={'class':'iti-eu-bld-gry'})
    
    if item_location:
       item_location = item_location.get_text().strip()
    else:
       item_location = "N/A"

    return item_location


def delivery_date(soup):
    # Returns the estimated date at which the product will be delivered to the DFW area
    # NOTE: the delivery date is calculated using the location of the computer that makes the page request
    
    delivery_date = soup.find('span', attrs={'class':'vi-acc-del-range'})
    
    if delivery_date:
       delivery_date = delivery_date.get_text().replace(u'and', u'-')
    else:
       delivery_date = "N/A"

    return delivery_date


def return_policy(soup):
    # Returns the return policy offered by the seller
    
    return_policy = soup.find('span', attrs={'id':'vi-ret-accrd-txt'})
    
    if return_policy:
       return_policy = return_policy.get_text().replace(u'\xa0', u' ').strip()
       if len(return_policy) > 79:
           return_policy = return_policy[:79] + "..."

    else:
       return_policy = "N/A"

    return return_policy

def date_and_time():
    # Returns the current date and time as a tuple (date, time)
    
    mydate = time.strftime("%m/%d/%Y", localtime())
    mytime = time.strftime("%H:%M:%S", localtime())
    
    return (mydate, mytime)
