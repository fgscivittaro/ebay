import requests
from bs4 import BeautifulSoup
from datetime import date, time

def ebay_scraper(url):
   req = requests.get(url)
   soup = BeautifulSoup(req, html.parser)

   title = soup.find('h1', attrs={class:'it-ttl'})
   title.get_text()

   subtitle = soup.find('h2', attrs={id='subTitle'})
   subtitle.get_text()

   item_rating = soup.find('span', attrs={class:'reviews-seeall-hdn'})
   item_rating.get_text()

   how_many_ratings = soup.find('a', attrs={class:"prodreview vi-VR-prodRev"})
   how_many_ratings.get_text()

   seller_name = soup.find('span', attrs={class:'mbg-nw'})
   seller_name.get_text()

   seller_reviews = soup.find('span', attrs={class:'mbg-1'})
   seller_link = seller_reviews.find('a')
   seller_reviews = seller_link.get_text()

   seller_percent_feedback = soup.find('div', attrs={id:'si-fb'})
   seller_percent_feedback.get_text()

   hot_info = soup.find('div', attrs={id:'vi_notification_new'})
   hot_info.get_text()

   condition = soup.find('div', attrs={class:"u-flL condText  "})
   condition.get_text()

   amount_sold = soup.find('span', attrs={class:"vi-qtyS vi-bboxrev-dsplblk vi-qty-vert-algn vi-qty-pur-lnk"})
   amount_sold.get_text()

   amount_available = soup.find('span', attrs={id:'qtySubTxt'})
   amount_available.get_text()

   trending_price = soup.find('span', attrs={class:'mp-prc-red}')
   trending_price.get_text()

   list_price = soup.find('span', attrs={id:'orgPrc'})
   list_price.get_text()

   you_save = soup.find('span', attrs={id:'youSaveSTP'})
   you_save.get_text()

   now_price = soup.find('span', attrs={id:'prcIsum'})
   now_price.get_text()

   total_watching = soup.find('span', attrs={class:'vi-buybox-watchcount'})
   total_watching.get_text()

   shipping_cost = soup.find('span', attrs={id:fshippingCost})
   shipping_cost.get_text()
   if shipping_cost=="FREE":
       shipping_cost = '0'

   shipping_type = soup.find('span', attrs={id:'fShippingSvc'})
   shipping_type.get_text()

   item_location = soup.find('div', attrs={class:'iti-eu-bld-gry'})
   item_location.get_text()

   delivery_date = soup.find('strong', attrs={class:"sh_med_font vi-acc-del-range"})
   delivery_date.get_text()
   #The estimated delivery date is based on my location; is this information
   #therefore at all relevant to our insights of other buyers//sellers?

   return_policy = soup.find('span', attrs={id:'vi-ret-accrd-txt'})
   return_policy.get_text()

   ebay_item_number = soup.find('div', attrs={id:'descItemNumber'})
   ebay_item_number.get_text()

   shipping_tab = soup.find('li', attrs={class:'item'})
   tab_link = shipping_tab.find('a')
   tab_link.get_link()

   inquiries = soup.find('span', attrs={class:'w2b-sgl'})
   inquiries.get_text()

   date = datetime.date
   time = datetime.time
