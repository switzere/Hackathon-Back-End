#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
from io import BytesIO

def get_webpages(webpage) -> dict:
    """
    This function returns the resulting dom for a webpage.
    """
    page = requests.get(webpage)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup

def scrape_US() -> list:
    """
    scrapes the data from the us travel website
    """

    data = get_webpages("https://travel.state.gov/content/travel/en/us-visas/tourism-visit/visa-waiver-program.html")
    us_li = []
    stripped_li = []
    li = data.find_all("ul")

    us_li = li[16].text + li[17].text + li[18].text
    us_li = us_li.split("\n")
    us_li = list(filter(None, us_li))

    for new_ul in us_li:
        stripped_li.append(new_ul.replace('*', ''))

    return stripped_li

def scrape_canada() -> list:
    """
    scrapes the data froms the canadian immigration website
    """
    ctr = 0
    data2 = []
    found = False
    data = get_webpages(
        "https://www.canada.ca/en/immigration-refugees-citizenship/services\
        /visit-canada/entry-requirements-country.html#visaExempt"
        )
    data = data.body.find_all("ul")
    for line in data:
        #print(line)
        for l in line.findChildren("li"):
            if ctr == 3:
                data2.append(l.text)
                found = True
            if ">eTA exemptions</a" in str(l):
                ctr += 1
        if found is True:
            break
    return data2

def scrape_EU() -> list:
    """
    scrapes the data from the worldtravelguide because the EU website doesn't allow bots
    """

    data = get_webpages("https://www.worldtravelguide.net/features/feature/travelling-to-europe-without-a-visa/")

    li = data.find_all("ul")


    eu_li = li[2].text + li[3].text + li[4].text + li[5].text


    eu_li = eu_li.split("\n")
    eu_li = list(filter(None, eu_li))

    return eu_li


def main():

    US_list = scrape_US()
    CA_list = scrape_canada()
    EU_list = scrape_EU()
    print(EU_list)




if __name__ == "__main__":
    main()
