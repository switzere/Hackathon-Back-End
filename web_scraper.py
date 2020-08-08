#!/usr/bin/env python3
import requests
import re
from bs4 import BeautifulSoup
import json


def get_webpages(webpage) -> dict:
    """
    This function returns the resulting dom for a webpage.
    """
    page = requests.get(webpage)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup

def scrape_US() -> list:
    data = get_webpages("https://travel.state.gov/content/travel/en/us-visas/tourism-visit/visa-waiver-program.html")
    us_li = []
    stripped_li = []
    li = data.find_all("ul")

    us_li = li[16].text + li[17].text + li[18].text
    us_li = us_li.split("\n")
    us_li = list(filter(None, us_li))

    for new_ul in us_li:
        stripped_li.append(new_ul.replace('*', ''))
        #print(''.join(filter(str.isalnum, new_ul)))
    #us_li = [re.sub("*","",x) for x in us_li]

    print(stripped_li)

    return stripped_li

def main():

    US_list = scrape_US()
    print(US_list)


if __name__ == "__main__":
    main()
