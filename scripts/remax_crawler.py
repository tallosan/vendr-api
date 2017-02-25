#
#	ReMax web crawler.
#
#	We have two operations here:
#	1.) Get listings (i.e. get the URLs for each individual
#	   property listing).
#	2.) Get property info (i.e. Go to the listing pages and parse
#	   the property data.
#
######################################################################


import time

import cPickle as pickle

import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select

cdriver_path 	= '/home/john/Downloads/chromedriver'
driver		= webdriver.Chrome(executable_path=cdriver_path)
driver.implicitly_wait(10)


'''	Waits for AJAX. '''
def wait_ajax():

	timeout = time.time() + 30
	
	# Sleep until the Ajax has loaded. If nothing has happened after 30
	# seconds, we can safely assume that we can continue.
	while not driver.execute_script('return jQuery.active == 0;'):
		if time.time() > timeout:
			return

#=================================================================================

'''	Parses a file containing GTA regions, and returns each line in a list.
	Args:
		fname: The name of the file to be parsed.
'''
def parse_regions(fname):

	regions = []
	with open(fname, 'rb') as fp:
		for line in fp.readlines():
			regions.append(line.strip('\n'))

	return regions


'''	Crawl the ReMax site for the given queries.
	Args:
		queries: The search queries.
'''
def get_listings(queries):

	listings = []
	
	province = ', ON'
	for query in queries:
		listings += get_region_listings(query + province)

	return listings

'''	Perform a search on a given query.
	Args:
		query: The query to search.
'''
def get_region_listings(query):

	base_url = 'http://www.remax.ca/on/'
	driver.get(base_url)
	
	# Set the search filter to 'For Sale'.
	search_filter = Select(driver.find_element_by_id('searchFilterSelection'))
	search_filter.select_by_value('forSale')

	# Enter the search query into the search bar, and perform search.
	search_input = driver.find_element_by_id('search-query')
	search_input.send_keys(query)
	driver.find_element_by_id('searchButton').click()
	
	# Sleep until the URL has fully loaded, then switch the view to 
	# 'gallery' mode. Bit of a hack, but it's the cleanest solution.
	while 'listingtab.index' not in driver.current_url: pass
	driver.get(driver.current_url[:-1] + '0')
	
	return parse_listing_pages()


'''	Parse all listings in a given region. N.B. -- We assume that the
	driver is on the correct starting page when this is called. '''
def parse_listing_pages():

	n_pages = get_n_pages()

	# Go through each page, and get the URLs for each property listed.
	listings = []
	for page in range(n_pages):
		wait_ajax()
		page += 1
		
		#TODO: We're getting both web, & mobile, elements. This gives us
		#      duplicates. Figure out how to just get one.
		gallery = driver.find_elements_by_class_name('teasersContainer')[0]
		for listing in gallery.find_elements_by_class_name('teaserImage'):
			listings.append(
				listing.find_element_by_css_selector('a').\
				get_attribute('href')
			)
		
		# Go to the next page.
		next_page(page)

	# This is a bit of a hack. We simply return the list w/out the duplicates.
	return listings[::2]

'''	Get the number of listing pages for a given region. '''
def get_n_pages():

	wait_ajax()
	n_pages = driver.find_element_by_class_name('pager')
	return int(n_pages.find_elements_by_tag_name('a')[-2].text)


'''	Jump to the next page.
	Args:
		cur_page: The page number we are currently on.
'''
def next_page(cur_page):
	
	wait_ajax()
	pager = driver.find_element_by_class_name('pager')
	next_page = pager.find_elements_by_css_selector('a')
	for element in next_page:
		if element.get_attribute('data-page') != None and \
		   int(element.get_attribute('data-page')) == (cur_page + 1):
			actions = ActionChains(driver).move_to_element(element)
			actions.click(element).perform()
			return

#=================================================================================

''' Parse the individual listing pages.
    args:
	    listings: The URLs of each listing to be parsed.
'''
def parse_listings(listings):

	data = []
	for listing in listings:
		print listing
		data += parse_listing(listing)

	print '[', len(data), ']'
	print data[0], '\t', data[1]
	return data


''' Parse a listing page, and return a tuple of x & y values, formatted as such ...
    	    ( [listing data] , listing_price )
    args:
	    listing: The URL of the listing to be parsed.
'''
def parse_listing(listing):

	driver.get(listing)
	wait_ajax()

	pdesc = driver.find_element_by_class_name('property-description')
	
	# Y-Value / label.
	price		= format_price(pdesc.find_element_by_css_selector('h3').text)
	
	# X-Values.
	location 	= pdesc.find_element_by_class_name('propertyAddress')
	region, postal  = format_location(location.find_elements_by_css_selector('span'))
	names		= pdesc.find_elements_by_class_name('propertyName')
	values		= pdesc.find_elements_by_class_name('propertyValue')

	meta = {}
	for name, value in zip(names, values):
		meta[name.text[:-1]] = value.text
	
	for k in meta.keys():
		print k, ': ', meta[k]

	building_type	= meta['Building type']
	sqr_ftg		= format_sqr_ftg(meta['Living space'])
	garage_spaces	= meta['Garage Spaces']

	taxes		= meta['Taxes']
	
	n_kitchens	= meta['Kitchens']
	n_rooms		= meta['Rooms']
	n_bedrooms	= meta['Bedrooms']
	n_bathrooms	= meta['Bathrooms']

	aksdj;
	
	#TODO: Normalize numerical data w/standard deviation.
	#      (x - mean) / stddev

	return (x_values, price)

''' Takes in a price string, and formats it into an int.
    args:
        price: The price string, formatted as such: '$ ___,___'.
'''
def format_price(price):

	return int(''.join(price[1:].split(',')))


''' Takes in a block of location data, and formats it. We return the region as
    a one-hot vector, and the postal code as a tuple of longitute & latitude.
    args:
    	location: An array of location data points (e.g. [address, region, postal code]).
'''
def format_location(location):

	region	 = ''.join(location[1].text.split(' '))
	postal	 = ''.join(location[2].text.split(' '))
	print postal
	from geopy.geocoders import Nominatim
	import ssl

	context = ssl._create_unverified_context()
	geolocator = Nominatim()
	print geolocator.geocode(postal)
	
	#TODO: Encode region.
	#TODO: Find latitude and longitutde values.
	return region, postal


''' Takes in a value for the square footage, and returns a valid int value.
    args:
    	sqr_ftg: The square footage in a string format.
'''
def format_sqr_ftg(sqr_ftg):

	print sqr_ftg
	pass


#=================================================================================
#
# Default parameters.
REGION_FILE 	= 'scripts/gta_regions.txt'
LISTINGS_FILE	= 'listings.pkl'
GET_LISTINGS 	= True
LOAD_LISTINGS	= False

if GET_LISTINGS:
	regions		= parse_regions(REGION_FILE)
	listings	= get_listings(regions)

	with open(LISTINGS_FILE, 'wb') as fp:
		pickle.dump(listings, fp)

if LOAD_LISTINGS:
	with open(LISTINGS_FILE, 'rb') as fp:
		listings = pickle.load(fp)

	parse_listings(listings)


