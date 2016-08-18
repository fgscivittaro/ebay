import requests, time, re
from bs4 import BeautifulSoup
from time import localtime

def product(url):
   #Scrapes an eBay product page and returns the available information and data.
   soup = BeautifulSoup(requests.get(url).text, 'html.parser')

   #The product's unique item_number. Could be used as a key value.
   item_number = soup.find('div', attrs={'id':'descItemNumber'})
   item_number = item_number.get_text()

   print item_number

   #The product title.
   title = soup.find('h1', attrs={'class':'it-ttl'})
   for i in title('span'):
       i.extract()
   title = title.get_text()

   print title

   #The product's rating, out of five stars.
   item_rating = soup.find('span', attrs={'class':'reviews-seeall-hdn'})
   if item_rating:
       item_rating = item_rating.get_text().replace(u'\xa0', u' ')[:3]
   else:
       item_rating = 'N/A'

   print item_rating

   #The total number of ratings the product has received.
   total_ratings = soup.find('a', attrs={'class':"prodreview vi-VR-prodRev"})
   if total_ratings:
       total_ratings = total_ratings.get_text().replace(u',', u'')[:-7].strip()
   else:
       total_ratings = '0'

   print total_ratings

   #The seller's eBay username.
   seller_name = soup.find('span', attrs={'class':'mbg-nw'})
   if seller_name:
       seller_name = seller_name.get_text()
   else:
       seller_name = 'N/A'

   print seller_name

   #The total number of reviews the seller has received.
   seller_reviews = soup.find('span', attrs={'class':'mbg-l'})
   if seller_reviews:
       seller_reviews = seller_reviews.find('a').get_text()
   else:
       seller_reviews = "N/A"

   print seller_reviews

   #The seller's positive feedback rating, given as a percent.
   seller_feedback = soup.find('div', attrs={'id':'si-fb'})
   if seller_feedback:
       seller_feedback = seller_feedback.get_text().replace(u'\xa0', u' ')[:-19]
   else:
       seller_feedback = "N/A"

   print seller_feedback

   #The information given by eBay next to the "fire" emblem under the title.
   hot_info = soup.find('div', attrs={'id':'vi_notification_new'})
   if hot_info:
       hot_info = hot_info.get_text().strip().replace(u',', u'')
   else:
       hot_info = "N/A"

   print hot_info

   #The declared condition of the item.
   condition = soup.find('div', attrs={'class':"u-flL condText  "})
   if condition:
       condition = condition.get_text()
   else:
       condition = "N/A"

   print condition

   #How many units of the product have already been sold.
   amount_sold = soup.find('span', attrs={'class':"qtyTxt vi-bboxrev-dsplblk  vi-qty-fixAlignment"}).find('a')
   if amount_sold:
       amount_sold = amount_sold.get_text().replace(u',', u'')[:-5]
   else:
       amount_sold = "N/A"

   #Sometimes this will say "x sold in 24 hours", and the scraper returns only x.
   #Is this desirable, or should be also note that it is within a 24-hour period?
   print amount_sold

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

   print amount_available

   #The number of inquiries, if available.
   pattern = re.compile(r'inquiries')
   inquiries = soup.find(text=pattern)
   if inquiries:
       inquiries = inquiries.replace(u',', u'')[:-10]
   else:
       inquiries = "N/A"

   print inquiries

   #Scrapes the trending price of a kind of product whenever it is provided.
   trending_price = soup.find('div', attrs={'class':'u-flL vi-bbox-posTop2 '})
   if trending_price:
       for i in trending_price('div'):
           i.extract()
       trending_price = trending_price.get_text().strip().replace(u',', u'').replace(u'US ', u'')[1:]
   else:
       trending_price = "N/A"

   print trending_price

   #The original price of the product.
   list_price = soup.find('span', attrs={'id':['orgPrc', 'mm-saleOrgPrc']})
   if list_price:
       list_price = list_price.get_text().strip().replace(u'US ', u'').replace(u',', u'')[1:]
   else:
       list_price = "N/A"

   print list_price

   #The product discount, in both dollar and percent.
   you_save = soup.find('span', attrs={'id':'youSaveSTP'})
   if not you_save:
       you_save = soup.find('div', attrs={'id':'mm-saleAmtSavedPrc'})
   else:
       pass
   if you_save:
       you_save = you_save.get_text().strip().replace(u'\xa0', u' ').replace(u'US ', u'').replace(u',', u'')
       you_save_raw = you_save[1:-10]
       you_save_percent = you_save[-8:-6]
   else:
       you_save_raw = "N/A"
       you_save_percent = "N/A"

   print you_save_raw
   print you_save_percent

   #The product's current price, after discounts.
   now_price = soup.find('span', attrs={'id':'prcIsum'})
   if not now_price:
       now_price = soup.find('span', attrs={'id':'mm-saleDscPrc'})
   else:
       pass
   if now_price:
       now_price = now_price.get_text().replace(u',', u'')[4:]
   else:
       now_price = "N/A"

   print now_price

   #The product's shipping costs.
   shipping_cost = soup.find('span', attrs={'id':'fshippingCost'})
   shipping_cost = shipping_cost.get_text().strip().replace(u',', u'')
   if shipping_cost=="FREE":
       shipping_cost = '0.00'
   elif shipping_cost != "FREE":
       pass

   print shipping_cost

   #The total cost of the product: price plus shipping.
   if now_price != "N/A":
       total_cost = float(now_price) + float(shipping_cost)
       print("%.2f" % total_cost)
   else:
       total_cost = "N/A"
       print total_cost

   #The total number of buyers watching the product.
   total_watching = soup.find('span', attrs={'class':'vi-buybox-watchcount'})
   if total_watching:
       total_watching = total_watching.get_text().replace(u',', u'')
   else:
       total_watching = "N/A"

   print total_watching

   #The type of shipping that will be used for the product.
   shipping_type = soup.find('span', attrs={'id':'fShippingSvc'})
   if shipping_type:
       shipping_type = shipping_type.get_text().strip()
   else:
       shipping_type = "N/A"

   print shipping_type

   #The seller's location; where the item will be shipped from.
   item_location = soup.find('div', attrs={'class':'iti-eu-bld-gry'})
   if item_location:
       item_location = item_location.get_text()
   else:
       item_location = "N/A"

   print item_location

   #The estimated date at which the product will be delivered to the DFW area.
   delivery_date = soup.find('span', attrs={'class':'vi-acc-del-range'})
   if delivery_date:
       delivery_date = delivery_date.get_text().replace(u'and', u'-')
       #The estimated delivery date is based on my location; is this information
       #therefore at all relevant to our insights of other buyers//sellers?
   else:
       delivery_date = "N/A"

   print delivery_date

   #The return policy offered by the seller.
   return_policy = soup.find('span', attrs={'id':'vi-ret-accrd-txt'})
   if return_policy:
       return_policy = return_policy.get_text().replace(u'\xa0', u' ')
   else:
       return_policy = "N/A"

   print return_policy

   #The current date and time.
   mydate = time.strftime("%m/%d/%Y", localtime())
   mytime = time.strftime("%H:%M:%S", localtime())

   print mydate
   print mytime
