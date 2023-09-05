import xml.etree.ElementTree as ET
import sqlite3
import requests

# TODO: yohnanof, hazi heinam, maayan 2000, carrefour
# URLs needed
# https://www.mck.co.il/v2/retailers/1470/branches/2331/products?filters=%7B%22must%22:%7B%22term%22:%7B%22branch.isVisible%22:true%7D%7D%7D&from=1&size=500
urls = {'mck': 'https://www.mck.co.il', 'victory': 'https://www.victoryonline.co.il'}


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

    # Now getting all product info from victory api
    all_products = []
    while True:
        response = requests.get(url, params=params)
        data = response.json()

        if not data.get('products'):
            break  # Exit the loop if no more products

        # Process and store the products
        all_products.extend(data['products'])

        # Update pagination for the next request
        params['from'] += 500
        print(f"Scraped { params['from'] } products...")

    # Now, all_products contains all the scraped products
    return all_products


def insert_to_db(raw_data):
    # This function inserts the raw data into a new table
    conn = sqlite3.connect('/Users/deborahgironde/Downloads/data-full.sqlite')
    cursor = conn.cursor()
    cursor.execute('insert data to deborah.test_table')


def main(all_products):
    print(len(all_products))
    # Convert the other supermarket barcodes list to a set for faster membership checking
    other_supermarket_set = set(get_all())
    # filter products and keep only the ones that don't appear in the sqlite file.
    filtered_products = [product for product in all_products if product.get("barcode") not in other_supermarket_set]
    print(filtered_products, len(filtered_products))
    return filtered_products


if __name__ == "__main__":
    main(all_products=scrape(urls[input("Please enter the name of the supermarket: ")]))
    # TODO: convert and insert to table
