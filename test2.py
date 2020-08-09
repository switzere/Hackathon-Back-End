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
            country = country.text.split(" (")[0].split(".")[0].replace("\n",'')
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


def scrape_Peru() -> list:
    """
    scrapes the data for peru
    """
    countries = []
    data = get_webpages("https://visaguide.world/south-america/peru-visa/")
    data = data.body.findAll("ul")
    for line in data[8].findChildren("li"):
        countries.append(line.text.split(" (")[0].replace("*",''))
    return countries


def scrape_Korea() -> list:
    """
    scrapes the data for mexico
    """
    countries = []
    data = get_webpages("http://overseas.mofa.go.kr/ca-vancouver-en/brd/m_4542/view.do?seq=615041&srchFr=&srchTo=&srchWord=&srchTp=")
    data = data.body.findAll("table")[1]
    data = data.findAll("p")
    for line in data:
        line = line.text
        if "," in line:
            line = line.split(",")
            for item in line:
                item = item.split("(")[0].split("[")[0]
                countries.append(item.strip())
    return countries

def scrape_Mexico() -> list:
    countries = []
    ctr = 0
    data = get_webpages("https://www.visatraveler.com/visa-guides/mexico-visa-requirements/")
    data = data.body.findAll("div", {"class": "one-third"})
    for third in data:
        for line in str(third).split("<br/>"):
            if '<div class="one-third first">' in line:
                ctr += 1
            if ctr == 2:
                return countries
            line = line.replace("</div>","").replace("<div>","")
            if  ">" in line:
                line = line.split(">")[1].replace("</a","").strip()
            countries.append(line.strip())
    return countries

def scrape_wiki(url) -> list:
    countries = []
    data = get_webpages(url)
    data = data.body.findAll("table")[1]
    data = data.findAll("li")
    for line in data:
        countries.append(line.find("a").text)
    return countries

def scrape_South_Africa() -> list:
    """
    Scrape data for south africa
    """
    countries = []
    data = get_webpages("http://www.dha.gov.za/index.php/immigration-services/exempt-countries")
    data = data.body.findAll("table")[0]
    data = data.findAll("tr")
    for line in data:
        line = line.find("td").text
        if line != "Diplomatic" and "Visa" not in line and line != "COUNTRY NAME/ORGANISATIONS":
            if "United Kingdom of Great Britain and Northern Ireland" in line:
                line = "United Kingdom"
            elif "Russian Federation" in line:
                line = "Russia"
            countries.append(line.split("(")[0].split(",")[0].replace("*",''))
    return countries

def getEUCountries() -> None:
    """
    Get a list of European Union countries and add them to the database
    """
    countries = []

    cFind = []
    data = get_webpages("https://europa.eu/european-union/about-eu/countries_en")

    data = data.body.find(id="year-entry2")
    data = data.findAll("td")

    for line in data:
        countries.append(line.text)

    countries.pop()

    client = MongoClient('mongodb+srv://atlasAdmin:atlasPassword@lightningmcqueen.uc4fr.mongodb.net/LightningMcqueen?retryWrites=true&w=majority', 27017)
    db = client.get_database('Countries')

    for x in db["List of EU Countries"].find():
        if "Countries" in x:
            cFind = x["Countries"]
            break

    myquery = { "Countries": cFind }
    newvalues = { "$set": { "Countries": countries  } }

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
    input_country = input_country.replace(" ",'')
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
    for visa in visa_list:
        symbol = get_currency(visa)
        try:
            rate = c.get_rate(country,symbol)
        except Exception:
            rate = "??"
        final_list.append([visa, str(rate)])
    return final_list

def scraper(country) ->list:
    """
    returns list from scraper
    """
    data = []
    if country == "United States":
        data = scrape_US()
    elif country == "Canada":
        data = scrape_Canada()
    elif country == "Russia":
        data = scrape_Russia()
    elif country == "Japan":
        data = scrape_Japan()
    elif country == "European Union":
        data = scrape_EU()
    elif country == "Peru":
        data = scrape_Peru()
    elif country == "South Korea":
        data =  scrape_Korea()
    elif country == "Chad":
        data = scrape_wiki("https://en.wikipedia.org/wiki/Visa_policy_of_Chad")
    elif country == "South Africa":
        data = scrape_South_Africa()
    elif country == "Mexico":
        data = scrape_Mexico()
    elif country == "Brazil":
        data = scrape_wiki("https://en.wikipedia.org/wiki/Visa_policy_of_Brazil")
        data.append("European Union")
    elif country == "Jamaica":
        data = scrape_wiki("https://en.wikipedia.org/wiki/Visa_policy_of_Jamaica")
    elif country == "Uzbekistan":
        data = scrape_wiki("https://en.wikipedia.org/wiki/Visa_policy_of_Uzbekistan")
    return data


def main():
    countries = {
        "United States":"USD",
        "Canada":"CAD",
        "Russia":"RUB",
        "Japan":"JPY",
        "European Union":"EUR",
        "Peru":"SOL",
        "South Korea":"KRW",
        "Chad": "XAF",
        "South Africa": "ZAR",
        "Mexico": "MXN",
        "Brazil": "BRL",
        "Jamaica": "JMD",
        "Uzbekistan": "UZS"
        }
    for country in countries:
        country_list = scraper(country)
        country_list = currency_Exchange(countries[country], country_list)
        database(country_list, country)
    getEUCountries()

if __name__ == "__main__":
    main()
