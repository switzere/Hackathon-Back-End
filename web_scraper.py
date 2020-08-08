#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json


def get_webpages(webpage) -> dict:
    """
    This function returns the resulting dom for a webpage.
    """
    page = requests.get(f"http://www.{webpage}")
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup


def main():
    data = get_webpages("google.com")
    print(data)

if __name__ == "__main__":
    main()
