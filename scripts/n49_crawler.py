#	Email Parser.
#
#	Crawls the n49 website, extracting email addresses from its listed
#	businesses.
#
###############################################################################


import re	#TODO: Is this even used?

import selenium
from selenium import webdriver

# selenium web driver setup.
cdriver_path	 = '/Users/andrewtallos/Downloads/chromedriver'
driver		 = webdriver.Chrome(executable_path=cdriver_path)


'''	Get a list of search queries, e.g. ['contractor, 'inspector'].
	Args:
		fname: Name of the .xlsx file containing our search queries.
'''
def get_search_queries(fname):

	import xlrd
	import urllib2

	xl_workbook 	= xlrd.open_workbook(fname)
	worksheet	= xl_workbook.sheet_by_index(0)

	offset = 1	# Skip the header.
	rows   = []

	# Append each row, with special characters in the URL string
	# escaped using %xx.
	for i, row in enumerate(range(worksheet.nrows)):
		if i > offset:
			r = []
			for j, col in enumerate(range(worksheet.ncols)):
				r.append(worksheet.cell_value(i, j))
				r[-1] = urllib2.quote(r[-1].encode('utf-8'))
			
			rows.append(r)

	return rows


'''	Converts our search query terms into valid URLs.
	Args:
		queries: List of lists in the form [query_term, location]
'''
def linkify(queries):
	
	base_prefix = "https://www.n49.com/search/"
	suffixs = [
			"/253/Ajax/", "/459/Aurora/", "/422/Brampton/", 
			"/35025/Brock/", "/300/Burlington/", "/423/Caledon/",
			"262/Clarington/", "/31027/Georgina/", "/303/Halton Hills/",
			"/470/Markham/", "/305/Milton/", "/425/Mississauga/", 
			"/472/Newmarket/", "/307/Oakville/", "/268/Oshawa/",
			"/269/Pickering/", "/475/Richmond Hill/", "/699/Scarborough",
			"/33096/Scugog/", "/695/Toronto/", "/273/Uxbridge/",
			"/482/Vaughan/", "/274/Whitby/", "/483/Whitchurch-Soutffville/"
	]
	
	# Create URLs from the cartesian product of the query terms & the
	# different GTA regions.
	links = []
	for query in queries:
		for suffix in suffixs:
			links.append(base_prefix + query[0] + suffix)
	
	return links


'''	Return a list of html strings from a list of n49 API queries.
	Args:
		queries: List of URLs to query n49.
'''
def get_html(queries):
	
	# Create a list of URLs to individual business pages.
	email_links = []
	for query in queries:
		driver.get(query)
		
		n_results = driver.find_element_by_id('search-criteria-total-results')
		s_results = driver.find_element_by_class_name('search-results')
		scroll(s_results, int(n_results.text))
		
		links	  = [
				link.get_attribute('href')
				for link in s_results.
					find_elements_by_class_name('search-hit-image')
			    ]
		
		email_links += links
	
	return email_links


'''	Scrolls to the bottom of the page. n49 only shows a small fraction of the
	total search results unless you scroll down. Therefore, in order to obtain
	all of them, we simply need to scroll to the bottom of the page.
	Args:
		sr: The search results container. Gives us the # of elements inside.
		nr: The number of results to expect. We use this to know when to stop.
'''
def scroll(sr, nr):
	
	
	# Scroll through the page. n49 has a bug where the # of results listed
	# does not match the actual # of results. Breaking the loop after 1
	# minute solves this.
	import time
	timeout = time.time() + 60

	while len(sr.find_elements_by_class_name('search-hit-image')) < nr:
		driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
		if time.time() > timeout:
			return


'''	Recieves a list of individual business page URLs, and returns the
	their respective email addresses.
	Args:
		urls: List of URLs to individual business pages.
		verbose: Toggle for feedback.
'''
def get_emails(urls, verbose=False):
	
	# Extract the emails where possible. N.B. -- If no email is listed,
	# selenium will raise a NoSuchElement exception.
	emails = []
	for url in urls:
		if verbose: print url
		
		driver.get(url)
		try:
			email = driver.find_element_by_class_name('business-email')
			if email not in emails: emails.append(email.text)
		except selenium.common.exceptions.NoSuchElementException as NSE_error:
			if verbose: print str(NSE_error)
		
	return emails
	

if __name__=='__main__':
	
	queries 	= get_search_queries('contractors.xlsx')
	queries		= linkify(queries)
	urls		= get_html(queries)
	emails		= get_emails(urls, verbose=True)
	
	import cPickle as pickle
	with open('emails', 'w') as fp:
		pickle.dump(emails, fp)

	print emails
	print
	print len(emails), ' emails downloaded.'

