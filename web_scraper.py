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

    return stripped_li

def scrape_Canada() -> list:
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
        for l in line.findChildren("li"):
            if ctr == 3:
                data2.append(l.text)
                found = True
            if ">eTA exemptions</a" in str(l):
                ctr += 1
        if found is True:
            break
    return data2


def scrape_Russia() -> list:
    """
    scrapes visa data from the eu website
    """
    countries = []
    data = get_webpages(
        "https://www.visitrussia.org.uk/visas/getting-a-russian-visa/the-russian-federation-visa-free-regime/")
    data = data.body.find_all("ul")
    data = data[2]
    for child in data.findChildren("li"):
        for country in child.findChildren("p"):
            country = country.text.split(" ")[0].replace(".",'').replace("\n",'')
            country = country.split("\xa0")[0]
            countries.append(country)
    return countries

def scrape_Japan()-> list:
    """
    scrapes countries that dont require visa to enter japan
    """
    countries = []
    data = get_webpages("https://www.visasjapan.com/visa-exemptions/")
    data = data.body
    data = data.findAll(
        "ul")
    for line in data[4].findChildren("li"):
        countries.append(line.text)
    return countries

def main():
    """
    US_list = scrape_US()
    CA_list = scrape_Canada()
    RU_list = scrape_Russia()
    """
    JP_list = scrape_Japan()

if __name__ == "__main__":
    main()
