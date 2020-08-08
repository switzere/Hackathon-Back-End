#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
import pycurl
from io import BytesIO

def get_webpages(webpage) -> dict:
    """
    This function returns the resulting dom for a webpage.
    """
    page = requests.get(webpage)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup


def curl_stuff(website) -> dict:
    """
    uses curl because some websites are mean
    """
    b_obj = BytesIO()
    crl = pycurl.Curl()
    crl.setopt(crl.URL, website)
    crl.setopt(crl.WRITEDATA, b_obj)
    crl.setopt(pycurl.SSL_VERIFYPEER, 0)
    crl.setopt(pycurl.SSL_VERIFYHOST, 0)
    crl.perform()
    crl.close()
    get_body = b_obj.getvalue()
    print(get_body.decode('utf8'))
    soup = BeautifulSoup(get_body.decode('utf8'), 'html.parser')
    return soup

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
        print(line)
        for l in line.findChildren("li"):
            if ctr == 3:
                data2.append(l.text)
                found = True
            if ">eTA exemptions</a" in str(l):
                ctr += 1
        if found is True:
            break
    return data2


def scrape_eu()->list:
    """
    scrapes visa data from the eu website
    """
    data = curl_stuff("https://www.schengenvisainfo.com/etias/#countries-need-etias")
    data = data.body
    file =open("test.html","w")
    file.write(str(data))
    file.close()
    return data

def main():
    data = scrape_eu()
    print(data)
if __name__ == "__main__":
    main()
