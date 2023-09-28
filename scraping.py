# This code is scraping all the products for mck, victory, m2000, yenot bitan, tivtaam, ampm, keshet teamim & shuk city
# and then creates a json file containing all the raw data

import sqlite3
import json
import requests

# URLs needed
urls = {'mck': 'https://www.mck.co.il', 'victory': 'https://www.victoryonline.co.il',
        'm2000': 'https://www.m2000.co.il', 'yb': 'https://www.ybitan.co.il',
        'tivtaam': 'https://www.tivtaam.co.il', 'ampm': 'https://www.ampm.co.il',
        'keshet': 'https://www.keshet-teamim.co.il', 'shukcity': 'https://www.shukcity.co.il'}


def get_all():
    # get all existing barcodes from the sqlite file (change path)
    conn = sqlite3.connect('/Users/deborahgironde/Downloads/data-full.sqlite')
    cursor = conn.cursor()
    cursor.execute('select itemcode from items')
    existing_barcodes = [row[0] for row in cursor.fetchall()]
    conn.close()
    print(f"Extracted { len(existing_barcodes) } barcodes from db")
    return existing_barcodes


def scrape(supermarket):
    # Define url and params, branch will always be 2930 for internet
    url = f'{ supermarket }/v2/retailers/1470/branches/2930/products'
    params = {
        'filters': '{"must":{"term":{"branch.isVisible":true}}}',
        'from': 1,
        'size': 500
    }

    # Now getting all product info from api
    all_products = []
    while True:
        try:
            response = requests.get(url, params=params)
            data = response.json()

            if not data.get('products'):
                break  # Exit the loop if no more products

            # Process and store the products
            all_products.extend(data['products'])

            # Update pagination for the next request
            params['from'] += 500
            print(f"Scraped { params['from'] } products...")
        except Exception as e:
            print(e)

    # Now, all_products contains all the scraped products
    return all_products


def main(all_products):
    # Convert the other supermarket barcodes list to a set for faster membership checking
    other_supermarket_set = set(get_all())
    # filter products and keep only the ones that don't appear in the sqlite file.
    filtered_products = [product for product in all_products if product.get("barcode") not in other_supermarket_set]
    # dumps data into json file
    with open(f'./{supermarket}_data.json', 'w') as json_file:
        json.dump(filtered_products, json_file, indent=4)
        print('The data has been saved.')


if __name__ == "__main__":
    supermarket = input(f'please enter name of the supermarket ({urls.keys()}: ')
    main(all_products=scrape(urls[supermarket]))
