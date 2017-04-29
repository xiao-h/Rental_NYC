import pandas as pd
import urllib.request as ul
from bs4 import BeautifulSoup
import re

### Create mapping from zipcode to neighborhoods in NYC
url = "https://www.health.ny.gov/statistics/cancer/registry/appendix/neighborhoods.htm"
url_response=ul.urlopen(url, timeout=5)
soup = BeautifulSoup(url_response, 'html.parser')
table = soup.findAll("table")[0]
#borough: list of boroughs, neighborhood: list of neighborhoods, zip_code: list of zip codes
borough = list()
neighborhood = list()
zip_code = list()
zip_code_unique = list()
length = list()

#patterns for regular expressions - found printing table.find_all('tr')
pattern_borough = '"header1.+>(.+)</td>'
pattern_neighborhood = '"header2">\s(.+)</td>'
pattern_zip = '"header3">\s(.+)</td>'
regex_borough = re.compile(pattern_borough)
regex_neighborhood = re.compile(pattern_neighborhood)
regex_zip = re.compile(pattern_zip)

for line in table.findAll('td'):
    borough.extend(regex_borough.findall(str(line)))
    neighborhood.extend(regex_neighborhood.findall(str(line)))
    if len(neighborhood) > len(borough):
        borough.append(borough[-1])
    zip_code.extend(regex_zip.findall(str(line)))

for i in range(len(zip_code)):
    regex_zip2 = re.compile('(\s*[,]\s*)')
    zip_ext = regex_zip.sub(',', zip_code[i]).split(',')

    #list of unique zip codes
    zip_code_unique.extend(zip_ext)
    #number of split realized to get the corresponding borough and neighborhood
    length.append(len(zip_ext))

#code to duplicate the borough and neighborhood so that one given index gives both information
#must have a reverse loop to insert at the appropriate location
for i in range(len(borough))[::-1]:
    j = 0
    #j is a counter to insert the same borough/neighborhood at the given index
    while length[i] - j > 1:
        borough.insert(i, borough[i])
        neighborhood.insert(i, neighborhood[i])
        j += 1

for i in range(len(zip_code_unique)):
    if len(zip_code_unique[i]) == 6:
        zip_code_unique[i] = zip_code_unique[i][1:6]

neighborhood_lookup = pd.DataFrame(
    {'Borough': borough,
     'Neighborhood': neighborhood,
     'zip_code': zip_code_unique
    })

### merge df with neighborhood_lookup
neighborhood_lookup.to_csv('neighborhood_lookup.csv')
