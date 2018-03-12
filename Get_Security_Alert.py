#!/usr/bin/python
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import ssl

# This restores the same behavior as before.
context = ssl._create_unverified_context()


# res
time = '([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]'
pm_am = '(p\.m\.)|(a\.m\.)'
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
days_re = '|'.join(days)
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
months_re = '|'.join(months)
time_re = '(%s) (%s), (%s), (%s) [0-9]*' % (time, pm_am, days_re, months_re)
capitalized_word_re = '( [A-Z][a-zA-Z]*)'
address_re_1 = '\d{1,4}(%s)+ (Avenue|Street)' % capitalized_word_re
address_re_2 = '(%s)+ between \w+ (Avenue|Street) and \w+ (Avenue|Street)' % capitalized_word_re
address_re_3 = '\d{1,4}(%s)+ [a-zA-Z0-9_.]\s+ (Avenue|Street)' % capitalized_word_re


def get_security_alert():
    page = get_page("https://safety-security.uchicago.edu/services/security_alerts/")
    soup = BeautifulSoup(page, "html.parser")
    links = get_links(soup)

    title_info = []
    useful_body_info = []

    for link in links:
        link = BeautifulSoup(link, "html.parser")

        body = get_body(link)
        for single_body in body:
            title = get_title(single_body)
            useful_body = get_useful_body(single_body)

        title_info.append(title)
        useful_body_info.append(useful_body)

    return title_info, useful_body_info


def edit_security_alert():
    title_info, useful_body_info = get_security_alert()
    merged_list = to_string(title_info, useful_body_info)

    return merged_list

def get_page(url):
    fd = urlopen(url,context=context)
    content = fd.read()
    fd.close()
    return content.decode('utf8')

def get_links(soup):
    article = soup.find_all('article', class_="span9 main")[0]
    links = []
    for link in article.find_all('a'):
        sub_link = link.get('href')
        if 'update' not in sub_link:
            sub_page = get_page("https://safety-security.uchicago.edu/services/security_alerts/" + sub_link)
            links.append(sub_page)
    return links

def get_body(soup):
    return soup.find_all('article', class_="span6 main")

def get_title(soup):
    temp = soup.find_all('h2')
    return temp

def get_useful_body(soup):
    children = []
    temp = soup.find_all('p')
    for child in temp:
        sub_title = child.find_all('strong')
        if len(sub_title) > 0:

            children.append(child)
    return children

def to_string(list1, list2):
    new_list = []
    for i in range(len(list1)):
        list1[i] = str(list1[i])
        list2[i] = str(list2[i])
        if "Update" not in list1[i]:
            merged = (list1[i], list2[i])
            new_list.append(merged)
    return new_list

def extract():
    to_extract = edit_security_alert()
    result = []
    for text in to_extract:
        search_result = re.search(time_re, text[1])
        if search_result != None:
            line = [search_result.group(0)]
        else:
            line = ['']

        search_result = re.search(address_re_1, text[1])
        if search_result != None:
            line.append(search_result.group(0))
        else:
            search_between = re.search(address_re_2, text[1])
            if search_between != None:
                line.append(search_between.group(0))
            elif search_between == re.search(address_re_3, text[1]):
                if search_between != None:
                    line.append(search_between.group(0))
                else:
                    line.append('')

        result.append(line)

    print(result)


if __name__ == "__main__":
    extract()




