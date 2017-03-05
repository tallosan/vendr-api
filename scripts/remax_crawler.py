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

import numpy as np
import cPickle as pickle

import requests
import json

import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
cdriver_path    = '/home/john/Downloads/chromedriver'
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

	data_file = 'data.pkl'
	for listing in listings:
		print '\n', listing
		
		# Load the data file.
		with open(data_file, 'rb') as fp:
			data = pickle.load(fp)
		
		# Get the listing data, and write it to our data file.
		try:
			listing_data = parse_listing(listing)
			data.append(listing_data)
			print '-- \tadded ', '[', len(data), ']'
			with open(data_file, 'wb') as fp:
				pickle.dump(data, fp)
		except selenium.common.exceptions.NoSuchElementException as se:
			print '-- \terror', str(se)
		except selenium.common.exceptions.WebDriverException as se:
                        print '-- \terror', str(se)
		except ValueError as value_error:
			print '-- \terror', str(value_error)
                except Exception as general_exc:
                        print '-- \tunknown error: ', str(general_exc)
		
		print '[', len(data), ']'

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
	try:
		region, loc = format_location(
			location.find_elements_by_css_selector('span'))
		lat, lng	= loc
	except Exception:
		region, lat, lng = None, None, None
	names		= pdesc.find_elements_by_class_name('propertyName')
	values		= pdesc.find_elements_by_class_name('propertyValue')

	# Extract all data from the Property section.
	meta = {}
	for name, value in zip(names, values): meta[name.text[:-1]] = value.text
	
	# These are the x-values we are interested in.
	x_keys = {
			#'Building type': None,
			'Living space': None,
			#'Garage Spaces': None,
			#'Taxes': None,
			#'Kitchens': None,
			'Rooms': None,
			'Bedrooms': None,
			'Bathrooms': None
	}
	
	for x_key in x_keys.keys():
		try:
			if meta: x_keys[x_key] = meta[x_key]
		except KeyError as key_error:
			pass

	# Attempt to get the square footage.
        if x_keys['Living space']:
		x_keys['Living space'] = format_sqr_ftg(meta['Living space'])
	else:
		element = driver.find_element_by_class_name('simple-table')
		x_keys['Living space'] = get_square_footage(element)
	
	#if not x_keys['Garage Spaces']: x_keys['Garage Spaces'] = 0
	x_values = np.array(
			[
				x_keys['Living space'],
				lat, lng, #region,
				#x_keys['Building type'],
				#x_keys['Garage Spaces'],
				#format_price(x_keys['Taxes']),
				#format_rooms(x_keys['Kitchens']),
				format_rooms(x_keys['Rooms']),
				format_rooms(x_keys['Bedrooms']),
				x_keys['Bathrooms']
			], dtype='float64'
	)

	print x_keys
	print x_values
	if np.isnan(x_values).any():
		raise ValueError
	
	return (x_values, price)

''' Takes in a price string, and formats it into an int.
    args:
        price: The price string, formatted as such: '$ ___,___'.
'''
def format_price(price):
	
	try: return np.float64(''.join(price[1:].split(',')))
	except TypeError as type_error: pass
	
	return None


''' Takes in a block of location data, and formats it. We return the region as
    a one-hot vector, and the postal code as a tuple of longitute & latitude.
    args:
    	location: An array of location data points (e.g. [address, region, postal code]).
'''
def format_location(location):

	region	 = ''.join(location[1].text.split(' '))
	postal	 = ''.join(location[2].text.split(' '))
	
	BASE = 'http://maps.googleapis.com/maps/api/geocode/json?components=postal_code:'
	url  = BASE + postal
	r    = requests.get(url)
	json_data = json.loads(r.text)
	
	# Using the GoogleMaps API, get the longitude and latitude. If this fails, then
        # we will turn to an alternate source -- zip-codes.com.
	try:
		lat = json_data['results'][0]['geometry']['location']['lat']
		lng = json_data['results'][0]['geometry']['location']['lng']
	except IndexError as index_error:
		ALT = 'https://www.zip-codes.com/m/canadian/postal-code.asp?postalcode='
		r = requests.get(ALT + postal)
		i_lat, i_lng = r.text.index('Latitude:'), r.text.index('Longitude:')
		lat = r.text[i_lat + 20: i_lat + 29]
		lng = r.text[i_lng + 22: i_lng + 31]
		if lat[0] != '-': lat = lat[1:]
		if lng[0] != '-': lng = lng[1:]
		print 'ALTERNATE'
		print lat, lng

	#TODO: Encode region.
	return region, (lat, lng)


''' Takes in a value for the square footage, and returns a valid int value.
    args:
    	sqr_ftg: The square footage in a string format.
'''
def format_sqr_ftg(sqr_ftg_element):

	sqr_ftg = sqr_ftg_element.split('-')
	try:
		#return float(sqr_ftg[0]) + float(sqr_ftg[1].split()[0])
		return float(sqr_ftg[0]) + ((float(sqr_ftg[1]) - float(sqr_ftg[0]))/2)
	except ValueError as value_error:
		return float(sqr_ftg[0].split()[0])


''' Takes in an element containing the room dimensions, and returns the
    property's square feet.
    args:
    	element: The Web Element containing the room dimensions.
'''
def get_square_footage(element):

	table_values = element.find_elements_by_css_selector('tr')
	
	# Extract the room dimensions.
	dimensions = []
	sqr_ftg    = 0
	for tr in table_values[1:]:
		td = tr.text.split('X')
		try:
			dimensions.append(float(td[0].split()[-1]))
			dimensions.append(float(td[1].split()[0]))
		except Exception as exc:
			pass
		try:
			dimensions.append(float(td[0].split()[-2]))
			dimensions.append(float(td[1].split()[-2]))
		except Exception as exc:
			pass
			
	# Calculate the room dimensions (in metres), and sum the total
	# square feet of the property.
	if len(dimensions) == 0: return None
	while len(dimensions) > 0:
		dim0 = dimensions.pop(0)
		dim1 = dimensions.pop(0)
		sqr_ftg += (dim0 * dim1)
	
	# The conversion factor from metres to square feet.
	conv_to_square_feet = 10.7639
	return sqr_ftg * conv_to_square_feet


''' Format the rooms string. We have 2 cases to consider:
    a) The room is formatted as '# + #'. E.g. 3 + 1.
    b) Standard format '#'. E.g. 3
    args:
    	room_str: A string containing the number of rooms data.
'''
def format_rooms(room_str):
	
	try:
		if '+' in room_str:
			room_nums = room_str.split('+')
			return int(room_nums[0]) + int(room_nums[1])
		return int(room_str)
	except TypeError:
		return 1


#=================================================================================
#
# Default parameters.
REGION_FILE 	= 'scripts/gta_regions.txt'
LISTINGS_FILE	= 'listings.pkl'
GET_LISTINGS 	= True
LOAD_LISTINGS	= True

if GET_LISTINGS:
	regions		= parse_regions(REGION_FILE)
	listings	= get_listings(regions)

	with open(LISTINGS_FILE, 'wb') as fp:
		pickle.dump(listings, fp)

if LOAD_LISTINGS:
	with open(LISTINGS_FILE, 'rb') as fp:
		listings = pickle.load(fp)

	parse_listings(listings)

