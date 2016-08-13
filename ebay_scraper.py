import requests
from bs4 import BeautifulSoup
import time
from time import localtime
import re

def product(url):
   #Scrapes an eBay product page and returns the available information and data.

   soup = BeautifulSoup(requests.get(url).text, 'html.parser')

   #http://www.ebay.com/itm/Google-Chromecast-Wireless-Media-Streaming-Latest-Model-/222068980827?&_trksid=p2056016.m2516.l5255
   #http://www.ebay.com/itm/Merax-Finiss-Aluminum-21-Speed-700C-Road-Bike-Shimano-58cm-Black-Green-/182220370360?&_trksid=p2056016.m2516.l5255
   #http://www.ebay.com/itm/Huge-lot-of-300-old-vintage-Baseball-Cards-in-Unopened-Packs-/161230456539?hash=item258a1586db:g:9eEAAOxywh1TBmaB

   item_number = soup.find('div', attrs={'id':'descItemNumber'})
   item_number = item_number.get_text()

   print item_number

   title = soup.find('h1', attrs={'class':'it-ttl'})
   fluff = [s.extract() for s in title('span')]
   title = title.get_text()

   print title

   item_rating = soup.find('span', attrs={'class':'reviews-seeall-hdn'})
   if item_rating:
       item_rating = item_rating.get_text().replace(u'\xa0', u' ')[:3]
   else:
       item_rating = 'N/A'

   print item_rating

   total_ratings = soup.find('a', attrs={'class':"prodreview vi-VR-prodRev"})
   if total_ratings:
       total_ratings = total_ratings.get_text().replace(u',', u'')[:-7].strip()
   else:
       total_ratings = '0'

   print total_ratings

   seller_name = soup.find('span', attrs={'class':'mbg-nw'})
   if seller_name:
       seller_name = seller_name.get_text()
   else:
       seller_name = 'N/A'

   print seller_name

   #Scrapes the number of reviews the seller has received.
   seller_reviews = soup.find('span', attrs={'class':'mbg-l'})
   seller_reviews = seller_reviews.find('a').get_text()

   print seller_reviews

   #Scrapes the % positive feedback rating of a seller
   seller_feedback = soup.find('div', attrs={'id':'si-fb'})
   seller_feedback = seller_feedback.get_text().replace(u'\xa0', u' ')[:-19]

   print seller_feedback

   #Scrapes whatever information may be next to the fire emblem on the page.
   hot_info = soup.find('div', attrs={'id':'vi_notification_new'})
   if hot_info:
       hot_info = hot_info.get_text().strip().replace(u',', u'')
   else:
       hot_info = "N/A"

   print hot_info

   condition = soup.find('div', attrs={'class':"u-flL condText  "})
   condition = condition.get_text()

   print condition

   #Sometimes this will say "x sold in 24 hours", and the scraper returns only x.
   #Is this desirable, or should be also note that it is within a 24-hour period?
   amount_sold = soup.find('span', attrs={'class':"qtyTxt vi-bboxrev-dsplblk  vi-qty-fixAlignment"}).find('a')
   if amount_sold:
       amount_sold = amount_sold.get_text().replace(u',', u'')[:-5]
   else:
       amount_sold = "N/A"

   print amount_sold

   amount_available = soup.find('span', attrs={'id':'qtySubTxt'})
   amount_available = amount_available.get_text().strip()
   if amount_available=="More than 10 available":
      amount_available = ">10"
   elif amount_available=="Limited quantity available":
      amount_available = "Limited quantity"
   elif amount_available=="Last one":
      amount_available = "1"
   else:
      amount_available = amount_available[:-10]

   print amount_available

   pattern = re.compile(r'inquiries')
   inquiries = soup.find(text=pattern)
   if inquiries:
       inquiries = inquiries.replace(u',', u'')[:-10]
   else:
       inquiries = "N/A"

   print inquiries

   #http://www.ebay.com/itm/2-5-CT-Round-Cut-D-VS2-Diamond-Engagement-Ring-18k-White-Gold-Clarity-Enhanced-/371341421444?hash=item5675ac6b84:g:JtEAAOSwpDdVbGZz


   list_price = soup.find('span', attrs={'id':['orgPrc', 'mm-saleOrgPrc']})
   if list_price:
       list_price = list_price.get_text().strip().replace(u'US ', u'').replace(u',', u'')[1:]
   else:
       list_price = "N/A"

   print list_price

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

   now_price = soup.find('span', attrs={'id':'prcIsum'})
   if not now_price:
       now_price = soup.find('span', attrs={'id':'mm-saleDscPrc'})
   else:
       pass
   #if not now_price:
       #link = soup.find('a',text='See price on checkout')['href']
       #soup2 = BeautifulSoup(requests.get(link).text, 'html.parser')
       #now_price = soup2.find('td', attrs={'class':'vANBigp'})
   #else:
       #pass
   if now_price:
       now_price = now_price.get_text().replace(u',', u'')[4:]
   else:
       now_price = "N/A"

   print now_price

   shipping_cost = soup.find('span', attrs={'id':'fshippingCost'})
   shipping_cost = shipping_cost.get_text().strip().replace(u',', u'')
   if shipping_cost=="FREE":
       shipping_cost = '0.00'
   elif shipping_cost != "FREE":
       pass

   print shipping_cost

   if now_price != "N/A":
       total_cost = float(now_price) + float(shipping_cost)
       print("%.2f" % total_cost)
   else:
       total_cost = "N/A"
       print total_cost

   total_watching = soup.find('span', attrs={'class':'vi-buybox-watchcount'})
   total_watching = total_watching.get_text().replace(u',', u'')

   print total_watching

   shipping_type = soup.find('span', attrs={'id':'fShippingSvc'})
   shipping_type = shipping_type.get_text().strip()

   print shipping_type

   item_location = soup.find('div', attrs={'class':'iti-eu-bld-gry'})
   item_location = item_location.get_text()

   print item_location

   delivery_date = soup.find('span', attrs={'class':'vi-acc-del-range'})
   delivery_date = delivery_date.get_text().replace(u'and', u'-')
   #The estimated delivery date is based on my location; is this information
   #therefore at all relevant to our insights of other buyers//sellers?

   print delivery_date

   return_policy = soup.find('span', attrs={'id':'vi-ret-accrd-txt'})
   return_policy = return_policy.get_text().replace(u'\xa0', u' ')

   print return_policy

   mydate = time.strftime("%m/%d/%Y", localtime())
   mytime = time.strftime("%H:%M:%S", localtime())

   print mydate
   print mytime

   #Rarely ever appears. Not sure where to find it.
   #trending_price = soup.find('span', attrs={'class':'mp-prc-red}')
   #trending_price.get_text()
