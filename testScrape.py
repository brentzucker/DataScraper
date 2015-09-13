#!/usr/bin/env python
# -*- coding: utf-8 -*-

# easy_install pip
# pip install requests
# pip install BeautifulSoup4

import requests
from bs4 import BeautifulSoup

csv_file = open("websites.csv", 'w')
top_thousand = 1
top_ten_thousand = 10
top_million = 1000

def getWebsiteInfo(website):
	url2 = 'http://stuffgate.com/{0}'.format(website)
	page_html = requests.get(url2).text
	soup2 = BeautifulSoup(page_html, 'html.parser')
	revenue = value = created = expires = ''

	# Grab Names of Desired Values, the sibling has the value
	for tr in soup2(text='Annual Revenue'):
		revenue = tr.parent.find_next_sibling("td").string[:-4]
	for tr in soup2(text='Estimated Value'):
		value = tr.parent.find_next_sibling("td").string[:-4]
	for tr in soup2(text='Created:'):
		created = tr.parent.find_next_sibling("td").string
	for tr in soup2(text='Expires:'):
		expires = tr.parent.find_next_sibling("td").string
	
	return (revenue, value, created, expires)

if __name__ == '__main__':

	csv_file.write('Rank, Website, Advertisement Revenue, Estimated Value, Created, Expires')

	# Scrape the Ranks of the Top Websites
	for i in range(1, top_thousand + 1):
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

			# Get the info for the current website
			revenue, value, created, expires = getWebsiteInfo(website)

			# Log what Websites have been appended
			print {"rank": cells[1], "website": cells[3], "revenue": revenue, "value": value, "created": created, "expires": expires}

			# Append Website and Info to Websites List
			websites.append({"rank": cells[1], "website": cells[3], "revenue": revenue, "value": value, "created": created, "expires": expires})

		# Print in CSV format
		for w in websites:
			csv_file.write('{0}, {1}, {2}, {3}, {4}, {5}'.format(w['rank'], w['website'], w['revenue'], w['value'], w['created'], w['expires']))
		csv_file.close()
