#!/usr/bin/env python
# -*- coding: utf-8 -*-

# easy_install pip
# pip install requests
# pip install BeautifulSoup4

import requests, time
from bs4 import BeautifulSoup

top_thousand = 1
top_ten_thousand = 10
top_million = 1000
num_of_sites = top_thousand

# Returns information scraped from Wikipedia Article
def scrapeWikipedia(wikiArticle_name):
	# Empty String returned if not found
	industries = typeOfSite = owner = ''
	wiki_url = 'https://en.wikipedia.org/wiki/'

	if wikiArticle_name != '':
		scrape_url = '{0}{1}'.format(wiki_url, wikiArticle_name)
		page_html = requests.get(scrape_url).text
		soup = BeautifulSoup(page_html, 'html.parser')

		# If the infobox exists
		if len(soup.find_all("table", class_="infobox")) > 0:
			infobox = soup.find_all("table", class_="infobox")[0]

			for th in infobox(text='Industry'):
				# A list of industries or 1 industry
				if th.parent.find_next_sibling("td").string == None:
					# for link in th.parent.find_next_sibling("td").find_all('a'):
					industry_list = []
					for text in th.parent.find_next_sibling("td")(text=''):
						if text.string != None:
							industry_list.append(text.string)
					for industry in set(industry_list):
						industries += industry.string + ' - '
					industries = industries[:-3]
				else:
					industries = th.parent.find_next_sibling("td").string

			for text in infobox(text='Type of site'):		
				if hasattr(text.parent.parent.find_next_sibling("td"), 'string') and text.parent.parent.find_next_sibling("td").string != None:
					typeOfSite = text.parent.parent.find_next_sibling("td").string

			for text in infobox(text='Owner'):
				if text.parent.find_next_sibling("td").string != None:
					owner = text.parent.find_next_sibling("td").string
				elif len(text.parent.find_next_sibling("td")(text='')) > 0:
					owner = text.parent.find_next_sibling("td")(text='')[0].string

	return industries.encode('utf-8'), typeOfSite.encode('utf-8'), owner.encode('utf-8')

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
	csv_file.write('Rank, Website, Industry, Type Of Site, Owner, Google Pagerank, Advertisement Revenue, Estimated Value, Created, Expires\n')
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
			industries, typeOfSite, owner = scrapeWikipedia(website)

			# Get the info from stuffgate for the current website
			google_pr, revenue, value, created, expires = getWebsiteInfo(website)

			w = {"rank": cells[1], "website": cells[3], "industry": industries, "typeOfSite": typeOfSite, "owner": owner, "google_pr": google_pr, "revenue": revenue, "value": value, "created": created, "expires": expires}

			# Log what Websites have been appended
			print w

			# Append Website and Info to Websites List
			websites.append(w)

			# Write to CSV file
			csv_file = open(filename, 'a')
			csv_file.write('{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8} {9}\n'.format(w['rank'], w['website'], w['industry'], w['typeOfSite'], w['owner'], w['google_pr'], w['revenue'], w['value'], w['created'], w['expires']))
			csv_file.close()
