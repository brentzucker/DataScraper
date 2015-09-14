#!/usr/bin/env python
# -*- coding: utf-8 -*-

# http://pygoogle.googlecode.com/svn/trunk/ get pygoogle.py and setup.py
# python setup.py build
# sudo python setup.py install

# easy_install pip
# pip install requests
# pip install BeautifulSoup4

from pygoogle import pygoogle
import requests, time
from bs4 import BeautifulSoup

top_thousand = 1
top_ten_thousand = 10
top_million = 1000
num_of_sites = top_thousand

def getGoogleSearchResult(domain):
	# Empty string returned if not found
	wikiArticle_name = '' 

	# Search google for website's wikipedia page
	g = pygoogle('wikipedia: {0}'.format(domain))
	g.pages = 1

	# If there are results store the first results url
	if len(g.get_urls()) > 0:
		first_result = g.get_urls()[0]

		# Get the name of the Wikipedia Article by removing the preceding url
		wikiArticle_name = first_result[len('https://en.wikipedia.org/wiki/'):]
	return wikiArticle_name

# Returns information scraped from Wikipedia Article
def scrapeWikipedia(wikiArticle_name):
	# Empty String returned if not found
	industries = ''
	wiki_url = 'https://en.wikipedia.org/wiki/'

	if wikiArticle_name != '':
		scrape_url = '{0}{1}'.format(wiki_url, wikiArticle_name)
		page_html = requests.get(scrape_url).text
		soup = BeautifulSoup(page_html, 'html.parser')

		soup.find_all("table", class_="infobox")
		infobox = soup.find_all("table", class_="infobox")[0]

		for th in infobox(text='Industry'):
			# A list of industries or 1 industry
			if th.parent.find_next_sibling("td").string == None:
				for link in th.parent.find_next_sibling("td").find_all('a'):
					industries += link.string + ' - '
				industries = industries[:-3]
			else:
				industries = th.parent.find_next_sibling("td").string
	return industries

def getWebsiteInfo(website):
	url2 = 'http://stuffgate.com/{0}'.format(website)
	page_html = requests.get(url2).text
	soup2 = BeautifulSoup(page_html, 'html.parser')
	google_pr = revenue = value = created = expires = ''

	# Grab Names of Desired Values, the sibling has the value.
	# Remove commas to keep csv clean
	for tr in soup2(text='Google Pagerank'):
		for img in tr.parent.find_next_sibling("td").children:
			google_pr = img['alt'].replace(',', '')
	for tr in soup2(text='Annual Revenue'):
		revenue = tr.parent.find_next_sibling("td").string[:-4].replace(',', '')
	for tr in soup2(text='Estimated Value'):
		value = tr.parent.find_next_sibling("td").string[:-4].replace(',', '')
	for tr in soup2(text='Created:'):
		created = tr.parent.find_next_sibling("td").string.replace(',', '')
	for tr in soup2(text='Expires:'):
		expires = tr.parent.find_next_sibling("td").string.replace(',', '')
	
	return (google_pr, revenue, value, created, expires)

if __name__ == '__main__':

	# Get current date/time for filename
	date_time = time.strftime("%Y-%m-%d_%H-%M-%S")
	filename = 'Top-{0}000-Websites-{1}.csv'.format(num_of_sites, date_time)
	csv_file = open(filename, 'w')
	csv_file.write('Rank, Website, Industry, Google Pagerank, Advertisement Revenue, Estimated Value, Created, Expires\n')
	csv_file.close()

	# Scrape the Ranks of the Top Websites
	for i in range(1, num_of_sites + 1):
		url = 'http://stuffgate.com/stuff/website/top-{0}000-sites'.format(i)
		page_html = requests.get(url).text

		soup = BeautifulSoup(page_html, 'html.parser')

		top_websites_table = soup.find_all('tbody')[0]

		websites = []
		for row in top_websites_table:
			# row is not an array, its a BeautifulSoup Object
			cells = []
			for cell in row:
				cells.append(cell.string)
			rank = cells[1]
			website = cells[3]

			# Get info from Wikipedia for the current website
			wikiArticle_name = getGoogleSearchResult(website)
			industries = scrapeWikipedia(wikiArticle_name)

			# Get the info from stuffgate for the current website
			google_pr, revenue, value, created, expires = getWebsiteInfo(website)

			w = {"rank": cells[1], "website": cells[3], "industry": industries, "google_pr": google_pr, "revenue": revenue, "value": value, "created": created, "expires": expires}

			# Log what Websites have been appended
			print w

			# Append Website and Info to Websites List
			websites.append(w)

			# Write to CSV file
			csv_file = open(filename, 'a')
			csv_file.write('{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}\n'.format(w['rank'], w['website'], w['industry'], w['google_pr'], w['revenue'], w['value'], w['created'], w['expires']))
			csv_file.close()
		
		# # Print in CSV format
		# for w in websites:
		# 	csv_file.write('{0}, {1}, {2}, {3}, {4}, {5}'.format(w['rank'], w['website'], w['revenue'], w['value'], w['created'], w['expires']))
		# csv_file.close()
