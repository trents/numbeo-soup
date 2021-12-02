# numbeo-soup
This script uses the Python BeautifulSoup library to extract specific city data from Numbeo.

To run, download numbeo.py and city-list.txt to the same directory and run with
python numbeo.py

It will create an output file called output.csv, a comma-delimited file in the format:
CityName,Price

By default the script extracts the price of a regular cappuccino from each city.  This can
be changed by altering the search string in the script.
