""" This script uses BeautifulSoup to parse through Numbeo pages and get a specific data point. """

import re
import time
import random
from bs4 import BeautifulSoup
import requests

# This section keeps the Numbeo server from being unhappy with us

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

# This specifies the string we're looking for in the table on each Numbeo page
# We can change this when we're looking for other data points from Numbeo

STRING_TO_MATCH = "Cappuccino "

# city-list.txt contains a list of cities we want to investigate
# Numbeo's URL format uses the city name directly, but sometimes uses weird formatting

city_file = open("city-list.txt", "r")
content = city_file.read()
city_list = content.split("\n")
city_file.close()
city_cap_value = {}

for city in city_list:

    # Handling data quirks and formatting URL
    if len(city) == 0:
        continue
    clean_city = city.replace(" ","-")
    url = "https://www.numbeo.com/cost-of-living/in/" + clean_city

    # Making the request
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')

    # Find the cell with our string in it, back out to the full row, then zoom in on the cost cell
    cap_cell = soup.body.findAll("td",string=re.compile(STRING_TO_MATCH))
    cap_row = cap_cell[0].parent
    children = cap_row.findChildren()
    cap_item = children[1].findChildren()
    cap_value = cap_item[0].text
    cap_value = cap_value[:-2]

    # print the results to stdout, then store in the city_cap_value dict
    print(city.strip() + ",$" + cap_value.strip())
    city_cap_value[city] = "$" + cap_value

    # This is here to keep the Numbeo server happy - it doesn't like too many requests
    time.sleep(random.randint(1,9))

# Write the results to output.txt and we're done!
with open("output.txt", 'w') as f:
    for key, value in city_cap_value.items():
        f.write('%s,%s\n' % (key, value))
