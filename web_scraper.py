#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
from pymongo import MongoClient

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

def scrape_Canada() -> list:
    """
    scrapes the data froms the canadian immigration website
    """
    ctr = 0
    data2 = []
    countries = []
    found = False
    data = get_webpages(
        "https://www.canada.ca/en/immigration-refugees-citizenship/services/visit-canada/entry-requirements-country.html#visaExempt"
        )
    data = data.body.find_all("ul")
    for line in data:
        for l in line.findChildren("li"):
            if ctr == 3:
                data2.append(l.text.split(",")[0])
                found = True
            if ">eTA exemptions</a" in str(l):
                ctr += 1
        if found is True:
            break
    for line in data2:
        if "British" in line and "United Kingdom" not in countries:
            countries.append("United Kingdom")
        elif "British" in line:
            pass
        elif "Hong Kong" in line:
            countries.append("Hong Kong")
        elif "Romania" in line:
            countries.append(line.split(' ')[0])
        else:
            countries.append(line)
    return countries

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


def scrape_Russia() -> list:
    """
    scrapes visa data from the eu website
    """
    countries = []
    data = get_webpages(
        "https://www.visitrussia.org.uk/visas/getting-a-russian-visa/the-russian-federation-visa-free-regime/")
    data = data.body.find_all("ul")
    for child in data[2].findChildren("li"):
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
    data = data.body.findAll("ul")
    for line in data[4].findChildren("li"):
        countries.append(line.text)
    return countries

def main():
    US_list = scrape_US()
    CA_list = scrape_Canada()
    RU_list = scrape_Russia()
    JP_list = scrape_Japan()
    EU_list = scrape_EU()

if __name__ == "__main__":
    main()
