
import requests
import urllib.parse as urlparse
from urllib.parse import parse_qs
from tinydb import TinyDB, Query
import time

db = TinyDB('./db.json')
base_url = 'https://www.walgreens.com/locator/v1/stores/search?requestor=search'
stores_table = db.table('stores_raw')
Query = Query()
STATE = 'CA'


def scrape_single_city(url):
    params = parse_qs(urlparse.urlparse(url).query)
    city = params['city'][0]
    print(f'Scrapping {city}')
    exists = len(stores_table.search(Query.city == city)) > 0
    if exists:
        print(f'{city} already in DB')
        return

    page = 1
    has_more_results = True
    stores = []
    while has_more_results:
        response = requests.post(base_url, {"requestType": "dotcom", "s": "100", "r": 20, "q": f"{city}, {STATE}",
                                            "p": page, "address": f"{city}, {STATE}"}).json()
        stores.extend(response['results'])
        has_more_results = response['summary']['hasMoreResult']
        if not has_more_results:
            break
        page += 1
        time.sleep(0.1)

    print(f'Found {len(stores)} stores')
    for store in stores:
        store['city'] = city
        store['state'] = STATE
    stores_table.insert_multiple(stores)


def scrape_all_cities(city_urls):
    for url in city_urls:
        scrape_single_city(url)


if __name__ == "__main__":
    urls = ['http:/www.walgreens.com/storelocator/find.jsp?requestType=locator&state=CA&city=ALAMEDA&from=localSearch']
    scrape_all_cities(urls)
