from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import ssl

# This restores the same behavior as before.
context = ssl._create_unverified_context()

def get_FBI_code():
    page = get_page("http://gis.chicagopolice.org/clearmap_crime_sums/crime_types.html#N14")
    soup = BeautifulSoup(page, "html.parser")
    crimes_type = get_body(soup, "td", "def")
    crimes_type_list = []
    for crime in crimes_type:
        type = get_body(crime, 'span', 'crimetype')
        condition_1 = get_body(crime, 'span', 'crimesPerson')
        condition_2 = get_body(crime, 'span', 'crimesProp')
        condition_3 = get_body(crime, 'span', 'crimesSoc')
        FBI = [type, condition_1, condition_3, condition_2]
        print(FBI)

        # print(condition_1)
        # print(condition_2)
        # print(condition_3)
        # print("look!!!!")
        # print(conditions)
        print("********************************")



    return soup


def get_page(url):
    fd = urlopen(url, context=context)
    content = fd.read()
    fd.close()
    return content.decode('utf8')

def get_body(soup, name, class_type):
    return soup.find_all(name, {'class' : class_type})

def get_herf(soup):
    new_soup = soup.find_all('a')
    return new_soup

if __name__ == "__main__":
    get_FBI_code()
