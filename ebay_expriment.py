import requests, time, re, schedule
from bs4 import BeautifulSoup
from time import localtime

with open("product_data.txt", "w") as initial_file:
   initial_file.write(
   "Time;Item number;Title;Condition;Trending price($);List price($);" +
   "Discount($);Discount(%);Current price($);Shipping cost($);" +
   "Item location;Estimated delivery;Return policy;Total item ratings;" +
   "Item rating;Total seller reviews;Seller positive feedback(%);" +
   "Hot info;Total watching;Units sold;Units remaining;Inquiries;Date" + "\n"
   )

def job():
    #Scrapes the eBay home page and returns a list of links from the home page's
    #Featured Collections, and every link within each collection.

    print "I'm starting the iteration"
    url1 = 'http://www.ebay.com/'
    ebaysoup = BeautifulSoup(requests.get(url1).text, 'html.parser')

    no_lazy = ebaysoup.find_all('div', attrs = {'class':'no-lazy'})
    featured_links = []

    #Returns the link of each Featured Collection displayed on the main page.
    for html_code in no_lazy:
        featured_links.append(html_code.find('a').get('href'))

    product_links = []
    final_links = []

    #Iterates through the link of each Featured Collection.
    for html_url in featured_links:
        html_soup = BeautifulSoup(requests.get(html_url).text, 'html.parser')

        """#Generates the URL of an xml ajax request responsible for retrieving some
        #but not all of the product links.
        editor = html_url[24:]
        slash = editor.index('/')
        editor = editor[:slash]
        col_code = html_url[-12:]
        lxml_url = 'http://www.ebay.com/cln/_ajax/2/%s/%s' % (editor, col_code)
        limiter = {'itemsPerPage':'30'}
        lxml_soup = BeautifulSoup((requests.get(lxml_url, params=limiter).content), 'lxml')"""

        #Iterates through all the URLs found within the HTML code and appends them.
        item_thumb = html_soup.find_all('div', attrs={'class':'itemThumb'})
        for html_code in item_thumb:
            product_links.append(html_code.find('a').get('href'))

        #Retrieves all the URLs that the xml code is responsible for.
        #final_links = [a["href"] for a in lxml_soup.select("div.itemThumb div.itemImg.image.lazy-image a[href]")]

        #Merges the lists and turns them into a set, since there is some overlap.
        product_links = list(set(product_links + final_links))
        print str(len(product_links)) + " links scraped"

    ended1 = re.compile(r'This listing has ended')
    ended2 = re.compile(r'This listing was ended')

    for url in product_links:
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        ended_listing1 = soup.find(text=ended1)
        ended_listing2 = soup.find(text=ended2)

        print url

        if ended_listing1 or ended_listing2:
            product_links.remove(url)
            print "Link removed" + "\n"
        else:
            #The product's unique item_number. Could be used as a key value.
            item_number = soup.find('div', attrs={'id':'descItemNumber'})
            if item_number:
                item_number = item_number.get_text()
            else:
                item_number = "N/A"

            #The product title.
            title = soup.find('h1', attrs={'class':'it-ttl'})
            if title:
                for i in title('span'):
                   i.extract()
                title = title.get_text().encode('ascii','replace')
            else:
                title = "N/A"

            print title

            #The product's rating, out of five stars.
            item_rating = soup.find('span', attrs={'class':'reviews-seeall-hdn'})
            if item_rating:
               item_rating = item_rating.get_text().replace(u'\xa0', u' ')[:3]
            else:
               item_rating = 'N/A'

            #The total number of ratings the product has received.
            total_ratings = soup.find('a', attrs={'class':"prodreview vi-VR-prodRev"})
            if total_ratings:
               total_ratings = total_ratings.get_text().replace(u',', u'').replace(u'product', u'')[:-7].strip()
            else:
               total_ratings = '0'

            #The seller's eBay username.
            seller_name = soup.find('span', attrs={'class':'mbg-nw'})
            if seller_name:
               seller_name = seller_name.get_text()
            else:
               seller_name = 'N/A'

            #The total number of reviews the seller has received.
            seller_reviews = soup.find('span', attrs={'class':'mbg-l'})
            if seller_reviews:
               seller_reviews = seller_reviews.find('a').get_text()
            else:
               seller_reviews = "N/A"

            #The seller's positive feedback rating, given as a percent.
            seller_feedback = soup.find('div', attrs={'id':'si-fb'})
            if seller_feedback:
               seller_feedback = seller_feedback.get_text().replace(u'\xa0', u' ')[:-19]
            else:
               seller_feedback = "N/A"

            #The information given by eBay next to the "fire" emblem under the title.
            hot_info = soup.find('div', attrs={'id':'vi_notification_new'})
            if hot_info:
               hot_info = hot_info.get_text().strip().replace(u',', u'')
            else:
               hot_info = "N/A"

            #The declared condition of the item.
            condition = soup.find('div', attrs={'class':"u-flL condText  "})
            if condition:
                for i in condition('span'):
                    condition = i.extract()
                condition = condition.get_text()
            else:
               condition = "N/A"

            #How many units of the product have already been sold.
            amount_sold = soup.find('span', attrs={'class':"qtyTxt vi-bboxrev-dsplblk  vi-qty-fixAlignment"})
            if amount_sold:
               amount_sold = amount_sold.find('a')
               if amount_sold:
                   amount_sold = amount_sold.get_text().replace(u',', u'')[:-5]
               else:
                   amount_sold = "N/A"
            else:
               amount_sold = "N/A"

            #How many available units of the product are left.
            amount_available = soup.find('span', attrs={'id':'qtySubTxt'})
            if amount_available:
               amount_available = amount_available.get_text().strip()
               if amount_available=="More than 10 available":
                  amount_available = ">10"
               elif amount_available=="Limited quantity available":
                  amount_available = "Limited quantity"
               elif amount_available=="Last one":
                  amount_available = "1"
               else:
                  amount_available = amount_available[:-10]
            else:
               amount_available = "N/A"

            #The number of inquiries, if available.
            pattern = re.compile(r'inquiries')
            inquiries = soup.find(text=pattern)
            if inquiries:
               inquiries = inquiries.replace(u',', u'')[:-10]
            else:
               inquiries = "N/A"

            #Scrapes the trending price of a kind of product whenever it is provided.
            trending_price = soup.find('div', attrs={'class':'u-flL vi-bbox-posTop2 '})
            if trending_price:
               for i in trending_price('div'):
                   i.extract()
               trending_price = trending_price.get_text().strip().replace(u',', u'').replace(u'US ', u'')[1:]
            else:
               trending_price = "N/A"

            #The original price of the product.
            list_price = soup.find('span', attrs={'id':['orgPrc', 'mm-saleOrgPrc']})
            if list_price:
               list_price = list_price.get_text().strip().replace(u'US ', u'').replace(u',', u'')[1:]
            else:
               list_price = "N/A"

            #The product discount, in both dollar and percent.
            you_save = soup.find('span', attrs={'id':'youSaveSTP'})
            if not you_save:
               you_save = soup.find('div', attrs={'id':'mm-saleAmtSavedPrc'})
            else:
               pass
            if you_save:
               you_save = you_save.get_text().strip().replace(u'\xa0', u' ').replace(u'US ', u'').replace(u',', u'')
               you_save_raw = you_save[1:-9].strip()
               you_save_percent = you_save.replace(you_save_raw, u'').replace(u'$',u'').replace(u'(',u'').replace(u'% off)',u'').strip()
            else:
               you_save_raw = "N/A"
               you_save_percent = "N/A"

            #The product's current price, after discounts.
            now_price = soup.find('span', attrs={'id':'prcIsum'})
            if not now_price:
               now_price = soup.find('span', attrs={'id':'mm-saleDscPrc'})
            else:
               pass
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
               else:
                   now_price = now_price[4:]
            else:
               now_price = "N/A"

            #The product's shipping costs.
            shipping_cost = soup.find('span', attrs={'id':'fshippingCost'})
            if shipping_cost:
                shipping_cost = shipping_cost.get_text().replace(u',', u'').replace(u'$', u'').strip()
                if shipping_cost[:3]=="GBP":
                    shipping_cost = soup.find('span', attrs={'id':'convetedPriceId'})
                    shipping_cost = shipping_cost.get_text()[4:]
                elif shipping_cost[1]=="C":
                    shipping_cost = soup.find('span', attrs={'id':'convetedPriceId'})
                    shipping_cost = shipping_cost.get_text()[4:]
                elif shipping_cost[:2]=="AU":
                    shipping_cost = soup.find('span', attrs={'id':'convetedPriceId'})
                    shipping_cost = shipping_cost.get_text()[4:]
                else:
                    if shipping_cost=="FREE":
                       shipping_cost = "0.00"
                    else:
                       pass
            else:
                shipping_cost = soup.find('span', attrs={'id':'shSummary'})
                if shipping_cost:
                    shipping = []
                    for i in shipping_cost('span'):
                        shipping.append(i.extract())
                    for i in shipping:
                        shipping_cost = i.get_text().strip()
                        if shipping_cost=="":
                            pass
                        else:
                            break
                else:
                    shipping_cost = "N/A"

            #The total number of buyers watching the product.
            total_watching = soup.find('span', attrs={'class':'vi-buybox-watchcount'})
            if total_watching:
               total_watching = total_watching.get_text().replace(u',', u'')
            else:
               total_watching = "N/A"

            #The seller's location; where the item will be shipped from.
            item_location = soup.find('div', attrs={'class':'iti-eu-bld-gry'})
            if item_location:
               item_location = item_location.get_text().strip()
            else:
               item_location = "N/A"

            #The estimated date at which the product will be delivered to the DFW area.
            delivery_date = soup.find('span', attrs={'class':'vi-acc-del-range'})
            if delivery_date:
               delivery_date = delivery_date.get_text().replace(u'and', u'-')
               #The estimated delivery date is based on my location; is this information
               #therefore at all relevant to our insights of other buyers//sellers?
            else:
               delivery_date = "N/A"

            #The return policy offered by the seller.
            return_policy = soup.find('span', attrs={'id':'vi-ret-accrd-txt'})
            if return_policy:
               return_policy = return_policy.get_text().replace(u'\xa0', u' ').strip()
               if len(return_policy)>90:
                   return_policy = return_policy[:90] + "..."
               else:
                   pass
            else:
               return_policy = "N/A"

            #The current date and time.
            mydate = time.strftime("%m/%d/%Y", localtime())
            mytime = time.strftime("%H:%M:%S", localtime())

            print "\n"

            with open("product_data.txt", "a") as continued_file:
                continued_file.write(
                    mytime + ";" +
                    item_number + ";" +
                    title + ";" +
                    condition + ";" +
                    trending_price + ";" +
                    list_price + ";" +
                    you_save_raw + ";" +
                    you_save_percent + ";" +
                    now_price + ";" +
                    shipping_cost + ";" +
                    item_location + ";" +
                    delivery_date + ";" +
                    return_policy + ";" +
                    total_ratings + ";" +
                    item_rating + ";" +
                    seller_reviews + ";" +
                    seller_feedback + ";" +
                    hot_info + ";" +
                    total_watching + ";" +
                    amount_sold + ";" +
                    amount_available + ";" +
                    inquiries + ";" +
                    mydate + "\n"
                    )

    print "I finished the iteration"

schedule.every(5).minutes.do(job)

job()

while True:
   schedule.run_pending()
   time.sleep(15)
