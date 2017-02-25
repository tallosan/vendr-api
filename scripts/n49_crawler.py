#	Email Parser.
#
#	Crawls the n49 website, extracting email addresses from its listed
#	businesses.
#
###############################################################################


import re	#TODO: Is this even used?
import cPickle as pickle

import selenium
from selenium import webdriver

# selenium web driver setup.
cdriver_path	 = '/home/john/Downloads/chromedriver'
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
			"/262/Clarington/", "/31027/Georgina/", "/303/Halton Hills/",
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
		url_file: The file containing our URLs.
                email_file: The file to store our emails.
		verbose: Toggle for feedback.
'''
def get_emails(url_file, email_file, verbose=False):
        
        empty = False
        while not empty:
                with open(url_file, 'rb') as fp:
                        urls = pickle.load(fp)

                if len(urls) <= 0: empty = True

                url     = urls.pop()
                email   = get_email(url, verbose=verbose)
                
                # If we get an email back, append it to our pickled file.
                if email:
                        with open(email_file, 'rb') as fp:
                                emails = pickle.load(fp)
                                emails.append(email)
                        with open(email_file, 'wb') as fp:
                                pickle.dump(emails, fp)

                with open(url_file, 'wb') as fp:
                        pickle.dump(urls, fp)


'''     Recieves a url and parses the email from it (if one is listed).
        Args:
                url: The URL of the page we're getting the URL from.
		verbose: Toggle for feedback.
'''
def get_email(url, verbose=False):
	
        if verbose: print url
	
        # Extract the emails where possible. N.B. -- If no email is listed,
	# selenium will raise a NoSuchElement exception.
        driver.get(url)
	try:
		email = driver.find_element_by_class_name('business-email')
                return email.text
                
        except selenium.common.exceptions.NoSuchElementException as NSE_error:
		if verbose: print str(NSE_error)
	except Exception as unknown_error:
		if verbose: print 'unknown error: ' + str(unknown_error)


#===================================================================================


GET_URLS      = False
GET_EMAILS    = False
FORMAT_EMAILS = True

URL_FILE      = 'urls.pkl'
EMAIL_FILE    = 'emails.pkl'
RESULTS_FILE  = 'emails.txt'

if GET_URLS:
    queries 	= get_search_queries('scripts/contractors.xlsx')
    queries		= linkify(queries)
    urls		= get_html(queries)
        
    # Save the URLs.
    with open(URL_FILE, 'wb') as fp:
        pickle.dump(urls, fp)

if GET_EMAILS:

    # Load the URLs.
    with open(URL_FILE, 'rb') as fp:
        urls = pickle.load(fp)

    emails = get_emails(url_file=URL_FILE, email_file=EMAIL_FILE, verbose=False)

if FORMAT_EMAILS:
    
    import collections

    # Load the emails.
    with open(EMAIL_FILE, 'rb') as fp:
        emails = list(set(pickle.load(fp)))

    # Write the emails to a file, separating each one with commas.
    with open(RESULTS_FILE, 'w') as fp:
        fp.write(','.join(emails))

