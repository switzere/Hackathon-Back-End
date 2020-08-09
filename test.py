#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
from pymongo import MongoClient
from forex_python.converter import CurrencyRates


def get_webpages(webpage) -> dict:
    """
    This function returns the resulting dom for a webpage.
    """
    page = requests.get(webpage)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup


def scrape_wiki(country) -> list:
    countries = []
    data = get_webpages(f"https://en.wikipedia.org/wiki/Visa_policy_of_{country}")
    try:
        data = data.body.findAll("table")[1]
        data = data.findAll("li")
        for line in data:
            countries.append(line.find("a").text.replace(" ","_"))
    except Exception:
        return []
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

def getEUCountries() -> None:
    """
    Get a list of European Union countries and add them to the database
    """
    countries = []
    cFind = []
    data = get_webpages(
        "https://europa.eu/european-union/about-eu/countries_en")

    data = data.body.find(id="year-entry2")
    data = data.findAll("td")

    for line in data:
        countries.append(line.text)

    countries.pop()

    client = MongoClient(
        'mongodb+srv://atlasAdmin:atlasPassword@lightningmcqueen.uc4fr.mongodb.net/LightningMcqueen?retryWrites=true&w=majority', 27017)
    db = client.get_database('Countries')

    for x in db["List of EU Countries"].find():
        if "Countries" in x:
            cFind = x["Countries"]
            break

    myquery = {"Countries": cFind}
    newvalues = {"$set": {"Countries": countries}}

    db["List of EU Countries"].update_one(myquery, newvalues)


def database(country_list, country) -> None:
    cFind = []

    client = MongoClient(
        'mongodb+srv://atlasAdmin:atlasPassword@lightningmcqueen.uc4fr.mongodb.net/LightningMcqueen?retryWrites=true&w=majority', 27017)
    db = client.get_database('Countries')
    if country in db.list_collection_names():
        for x in db[country].find():
            if "VisaFree" in x:
                cFind = x["VisaFree"]
                break

        myquery = {"VisaFree": cFind}
        newvalues = {"$set": {"VisaFree": country_list}}

        db[country].update_one(myquery, newvalues)
    else:
        my_dict = {"Name": country, "VisaFree": country_list}
        db[country].insert_one(my_dict)


def get_currency(input_country) -> str:
    """
    converts country to currency code
    """
    file = open("country_conversion.json", "r")
    data = json.load(file)
    file.close()
    input_country = input_country.replace(" ", '')
    if "UnitedStates" in input_country:
        input_country = "UnitedStates"
    elif "TheRepublicofSouthAfrica" in input_country or "RepublicofKorea" in input_country:
        input_country = "SouthKorea"
    elif "KirghizRepublic" in input_country:
        input_country = "Kyrgyzstan"
    elif "BruneiDarussalam" in input_country:
        input_country = "Brunei"
    elif "PitcairnIsland" in input_country:
        input_country = "Pitcairn"
    elif "Columbia" in input_country:
        input_country = "Colombia"
    for cntry in data:
        if cntry['Country'] == input_country:
            input_country = cntry['Code']
            break
    return input_country


def currency_Exchange(country, visa_list) -> list:
    """
    Pulls the currency data
    """
    final_list = []
    c = CurrencyRates()
    country = get_currency(country)
    for visa in visa_list:
        symbol = get_currency(visa)
        try:
            rate = c.get_rate(country, symbol)
        except Exception:
            rate = "??"
        final_list.append([visa, str(rate)])
    return final_list


def main():
    countries = []
    f = open("country_conversion.json", "r")
    data = json.load(f)
    for line in data:
        countries.append(line['Country'])
    for country in countries:
        country_list = scrape_wiki(country)

        if country_list:
            for line in data:
                if country in line:
                    country_list = currency_Exchange(line['Code'], country_list)
                    break
            #database(country_list, country)
    getEUCountries()
    country_list = scrape_EU()
    database(country_list, "European Union")
if __name__ == "__main__":
    main()
