import requests
from bs4 import BeautifulSoup

#Scrapes the eBay home page and returns a list of links from each Featured Collection page.
url = 'http://www.ebay.com/'
soup = BeautifulSoup(requests.get(url).text, 'html.parser')

no_lazy = soup.find_all('div', attrs = {'class':'no-lazy'})
featured_links = []

for link in no_lazy:
    featured_links.append(link.find('a').get('href'))

product_links = []

for link in featured_links:
    soup = BeautifulSoup(requests.get(link).text, 'html.parser')
    #For some reason, this does not return every single item.
    item_thumb = soup.find_all('div', attrs={'class':'itemThumb'})
    for link in item_thumb:
        product_links.append(link.find('a').get('href'))

print product_links

potential_problem = """<script escape-xml="true">
	  if (typeof(collectionState) != 'object') {
	      var collectionState = {
	          itemImageSize: {sWidth: 280, sHeight: 280, lWidth: 580, lHeight: 620},
	          page: 1,
	          totalPages: 2,
	          totalItems: 17,
	          pageId: '2057253',
	          currentUser: '',
	          collectionId: '324079803018',
	          serviceHost: 'svcs.ebay.com/buying/collections/v1',
	          owner: 'ebayhomeeditor',
	          csrfToken: '',
	          localeId: 'en-US',
	          siteId: 'EBAY-US',
	          countryId: 'US',
	          collectionCosEnabled: 'true',
	          collectionCosHostExternal: 'https://api.ebay.com/social/collection/v1',
	          collectionCosEditEnabled: 'true',
	          isCollectionReorderEnabled: 'false',
	          isOwnerSignedIn: false || false,
	          partiallySignedInUser: '@@__@@__@@',
	          baseDomain: 'ebay.com',
	          currentDomain: 'www.ebay.com',
	          isTablet: false,
	          isMobile: false,
              showViewCount: true
	      };
	  }
	</script>"""
