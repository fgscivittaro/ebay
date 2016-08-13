import requests
from bs4 import BeautifulSoup
import datetime
import time
from time import localtime

def product(url):
   #Scrapes an eBay product page and returns the available information and data.
   req = requests.get(url)
   soup = BeautifulSoup(req.text, 'html.parser')

   #http://www.ebay.com/itm/Google-Chromecast-Wireless-Media-Streaming-Latest-Model-/222068980827?&_trksid=p2056016.m2516.l5255
   #http://www.ebay.com/itm/Merax-Finiss-Aluminum-21-Speed-700C-Road-Bike-Shimano-58cm-Black-Green-/182220370360?&_trksid=p2056016.m2516.l5255

   #Should work in all cases, but need to check.
   item_number = soup.find('div', attrs={'id':'descItemNumber'})
   item_number = item_number.get_text()

   print item_number

   #Should work for all cases, but need to check.
   title = soup.find('h1', attrs={'class':'it-ttl'})
   [s.extract() for s in title('span')]
   title = title.get_text()

   print title

   #Works in specific case, but need to check for all cases.
   item_rating = soup.find('span', attrs={'class':'reviews-seeall-hdn'})
   if item_rating:
       item_rating = item_rating.get_text()
       item_rating = item_rating.replace(u'\xa0', u' ')
       item_rating = item_rating[:3]
   else:
       item_rating = 'N/A'

   print item_rating

   #Works in specific case, but need to check for all cases.
   total_ratings = soup.find('a', attrs={'class':"prodreview vi-VR-prodRev"})
   if total_ratings:
       total_ratings = total_ratings.get_text()
       total_ratings = total_ratings.strip()
       total_ratings = total_ratings[:-8]
   else:
       total_ratings = '0'

   print total_ratings

   #Works in specific case, but need to check for all cases.
   seller_name = soup.find('span', attrs={'class':'mbg-nw'})
   if seller_name:
       seller_name = seller_name.get_text()
   else:
       seller_name = 'N/A'

   print seller_name

   #Works in specific case, but need to check for all cases.
   #Scrapes the number of reviews the seller has received.
   seller_reviews = soup.find('span', attrs={'class':'mbg-l'})
   seller_link = seller_reviews.find('a')
   seller_reviews = seller_link.get_text()

   print seller_reviews

   #Scrapes the % positive feedback rating of a seller
   #Works in specific case, but need to check for all cases.
   seller_feedback = soup.find('div', attrs={'id':'si-fb'})
   seller_feedback = seller_feedback.get_text()
   seller_feedback = seller_feedback.replace(u'\xa0', u' ')
   seller_feedback = seller_feedback[:4]

   print seller_feedback

   #Should work for all cases, but need to check.
   #Scrapes whatever information may be next to the fire emblem on the page.
   hot_info = soup.find('div', attrs={'id':'vi_notification_new'})
   hot_info = hot_info.get_text()
   hot_info = hot_info.strip()

   print hot_info

   #Should work in all cases, but need to check.
   condition = soup.find('div', attrs={'class':"u-flL condText  "})
   condition = condition.get_text()

   print condition

   #Should work in all cases, but need to check.
   amount_sold = soup.find('span', attrs={'class':
   "qtyTxt vi-bboxrev-dsplblk  vi-qty-fixAlignment"})
   amount_sold = amount_sold.find('a')
   amount_sold = amount_sold.get_text()
   amount_sold = amount_sold[:-5]

   print amount_sold

   #Works in specific case, but need to check for all cases.
   amount_available = soup.find('span', attrs={'id':'qtySubTxt'})
   amount_available = amount_available.get_text()
   #What do we do if there are more than 10 available?
   amount_available = amount_available.strip()
   if amount_available=="More than 10 available":
      amount_available = ">10"
   elif amount_available=="Limited quantity available":
      amount_available = "Limited"
  elif amount_available=="Last one":
      amount_available = "1"
   else:
      amount_available = amount_available[:-10]

   print amount_available

   #http://www.ebay.com/itm/2-5-CT-Round-Cut-D-VS2-Diamond-Engagement-Ring-18k-White-Gold-Clarity-Enhanced-/371341421444?hash=item5675ac6b84:g:JtEAAOSwpDdVbGZz
   #Apparently this only works in some cases. Need to check in the diamond ring case.
   list_price = soup.find('span', attrs={'id':'orgPrc'})
   if list_price:
       list_price = list_price.get_text()
       list_price = list_price.strip()
       list_price = list_price[1:]
   else:
       list_price = "N/A"

   print list_price

   #Could work in all cases in which there is actually a sale, but need to check.
   you_save = soup.find('span', attrs={'id':'youSaveSTP'})

   if you_save:
       you_save = you_save.get_text()
       you_save = you_save.strip()
       you_save = you_save.replace(u'\xa0', u' ')
       you_save_raw = you_save[1:5]
       you_save_percent = you_save[7:9]
   else:
       you_save_raw = "N/A"
       you_save_percent = "N/A"

   print you_save_raw
   print you_save_percent

   #Could work in all cases, but need to make sure.
   now_price = soup.find('span', attrs={'id':'prcIsum'})
   now_price = now_price.get_text()
   now_price = now_price[4:]

   print now_price

   #Should work in all cases, but need to catch.
   shipping_cost = soup.find('span', attrs={'id':'fshippingCost'})
   shipping_cost = shipping_cost.get_text()
   shipping_cost = shipping_cost.strip()
   if shipping_cost=="FREE":
       shipping_cost = '0'
   else:
       pass

   total_cost = float(now_price) + float(shipping_cost)

   print shipping_cost
   print total_cost

   #Should work in all cases, but need to check.
   total_watching = soup.find('span', attrs={'class':'vi-buybox-watchcount'})
   total_watching = total_watching.get_text()

   print total_watching

   #Should work in all cases, but need to check.
   shipping_type = soup.find('span', attrs={'id':'fShippingSvc'})
   shipping_type = shipping_type.get_text()
   shipping_type = shipping_type.strip()

   print shipping_type

   #Should work in all cases, but need to check
   item_location = soup.find('div', attrs={'class':'iti-eu-bld-gry'})
   item_location = item_location.get_text()

   print item_location

   delivery_date = soup.find('span', attrs={'class':'vi-acc-del-range'})
   delivery_date = delivery_date.get_text()
   #The estimated delivery date is based on my location; is this information
   #therefore at all relevant to our insights of other buyers//sellers?

   print delivery_date

   #Will probably work for most cases, but need to check.
   return_policy = soup.find('span', attrs={'id':'vi-ret-accrd-txt'})
   return_policy = return_policy.get_text()
   return_policy = return_policy.replace(u'\xa0', u' ')

   print return_policy

   #'http://www.ebay.com/itm/Huge-lot-of-300-old-vintage-Baseball-Cards-in-Unopened-Packs-/161230456539?hash=item258a1586db:g:9eEAAOxywh1TBmaB'

   #Almost there, but not quite yet.
   inquiries = soup.find('div', attrs={'class':'w2b w2bsls'})
   inquiries = inquiries.find_all('span')
   inquiry_list = []
   for i in inquiries:
       for child in i.children:
           inquiry_list.append(child)
   #for i in inquiry_list:
       #if i==
        #  inquiries = i
       #else:
          #inquiries = 'N/A'

   print inquiry_list

   mydate = time.strftime("%m/%d/%Y", localtime())
   mytime = time.strftime("%H:%M:%S", localtime())

   #Rarely ever appears. Not sure where to find it.
   #trending_price = soup.find('span', attrs={'class':'mp-prc-red}')
   #trending_price.get_text()
