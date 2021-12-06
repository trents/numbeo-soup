""" This script uses BeautifulSoup to parse through Numbeo pages and get a specific data point. 
This script has a bunch of extra comments to help explain the details of the script to a new coder!
"""

import re # This imports a library that enables the use of regular expressions
          # Regular expressions are used for text pattern matching
import time # This imports a library for time-related functions
import random # This imports a random number generator
from bs4 import BeautifulSoup # This imports BeautifulSoup, which enables parsing of web pages
import requests # This imports a library that handles web requests

# This section keeps the Numbeo server from being unhappy with us
# The only line that's really import here is the 'User-Agent' line

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

# Open the city list text file for reading
city_file = open("city-list.txt", "r") 

# Read in the file contents to a string variable, content
content = city_file.read()

# Create a list called city_list and fill it with the individual lines from city-list.txt
# \n is the special character that means "end of line"
# so this one line is just breaking the contents from the file at each line break
# and creating a Python list of those individual lines
city_list = content.split("\n")

# Close the file
city_file.close()

# We're starting a simple dict here to store the output
# dict is a basic data structure in Python that stores things in key-value pairs 
# like a dictionary, storing words (key) and definitions (value) as pairs.
# This first entry is just put in there to function as the first header line of the file
# It creates a pair with key "City" and value equal to the string we're matching
city_cap_value = {"City":STRING_TO_MATCH}
                                         
# This is a for loop.  It runs through everything indented below it once for each
# item in city_list.  Within that loop, that specific item for that instance through
# the loop is known as city.
for city in city_list:

    # This first bit just skips any blank lines from the city-list.txt file.
    if len(city) == 0:
        continue

    # These two lines format the URL in a way that Numbeo likes
    # We're making a URL specifically for one city, the one this trip through the for loop
    # cares about
    clean_city = city.replace(" ","-")
    url = "https://www.numbeo.com/cost-of-living/in/" + clean_city

    # This makes the request to the server
    req = requests.get(url, headers)

    # This stores what the server sends back in a variable called soup
    soup = BeautifulSoup(req.content, 'html.parser')

    # This line finds the HTML table cell with our string in it and stores it as cap_cell
    # findAll is the search function in the BeautifulSoup library
    # td is the HTML component we're looking for - it basically means "table cell"
    # the re.compile part is simply saying "Find this string."
    cap_cell = soup.body.findAll("td",string=re.compile(STRING_TO_MATCH))

    # We now have the cell that contains the value we're searching for, but we really want
    # a different cell in the same row, the one that contains the dollar value of that item
    # So we back up a step and retrieve that full row
    cap_row = cap_cell[0].parent

    # We want all of the "children" of that row - in other words, all of the cells in that row
    children = cap_row.findChildren()

    # More specifically, we want the second cell in that row, which is children[1].
    # That's the cell that actually contains the value of a cup of cappuccino
    cap_item = children[1].findChildren()

    # cap_value is set as the value of that cell - the price of a cup of cappuccino
    cap_value = cap_item[0].text

    # This line removes the last two characters of that cell, which are junk
    cap_value = cap_value[:-2]

    # print the results to the screen
    print(city.strip() + ",$" + cap_value.strip())

    # store in the city_cap_value dict that we created earlier to store all of the city:cappuccino 
    # value pairs
    city_cap_value[city] = "$" + cap_value

    # This is here to keep the Numbeo server happy - it doesn't like too many requests
    time.sleep(random.randint(1,9))

    # ... and now we loop through again with the next city

# Write the results to output.txt and we're done!
with open("output.csv", 'w') as f:

    # Another for loop
    # This loops through everything stored in city_cap_value
    # Each time through the loop, the name of the city is stored in key
    # and the value of the cappuccino is stored in value
    for key, value in city_cap_value.items():

        # This line just writes the key and value in the format key,value
        # That way, it's a normal comma-delimited file that we can import easily into other things
        f.write('%s,%s\n' % (key, value))
