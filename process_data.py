# This code processes the raw data from the json files and inserts them to a table
# What we want to insert:
# description, nutrition itm (ingredients), symbole (sucar, shuman), unite de mesure, categorie, pct de fruits,
# marque, allergenes, may contain, image url

import sqlite3
import json


def process_json_data(json_file_path):
    data_list = []

    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

        # This helper function will return None if a key is not found in the JSON
        def get_key_or_none(dictionary, key):
            return dictionary.get(key, None)

        for item in data:
            try:
                product_data = {}
                product_data['barcode'] = item['barcode']
                product_data['ingredients'] = item['data']['1']['ingredients']
                product_data['unit_of_measure'] = get_key_or_none(item['UnitOfMeasure']['defaultName']) #we can change it to id
                product_data['brand'] = get_key_or_none(item['brand']['names']['2'])
                product_data['allergens'] = get_key_or_none(item['data']['1']['containAllergens'])
                product_data['image_url'] = item['image']['url']

                # Extract all names for product
                names = []
                for name in item['names']:
                    names.append(name['short'])

                # Extract all categories for product
                categories_list = []
                for categories in item['family']['categories']:
                    categories_list.append([categories['names']['2'], categories['names']['1']])

                # same for nutrition values
                nutr_values = item['nutritionValues']

                data_list.append(product_data)

            except KeyError:
                print('Key does not exist for this item')

    return data_list


# Define a function to insert data into an SQLite database
def insert_to_sqlite(data_list, db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create a table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                        description TEXT,
                        ingredients TEXT,
                        symbol TEXT,
                        unit_of_measure TEXT,
                        categorie TEXT,
                        pct_de_fruits REAL,
                        marque TEXT,
                        allergenes TEXT,
                        may_contain TEXT,
                        image_url TEXT
                    )''')

    # Insert data into the table
    for product_data in data_list:
        cursor.execute('''INSERT INTO products (description, ingredients, symbol, unit_of_measure, categorie, 
                        pct_de_fruits, marque, allergenes, may_contain, image_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (product_data['description'], product_data['ingredients'], product_data['symbol'],
                        product_data['unit_of_measure'], product_data['categorie'], product_data['pct_de_fruits'],
                        product_data['marque'], product_data['allergenes'], product_data['may_contain'], product_data['image_url']))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    json_file_path = './mck_data.json'
    db_file = 'your_database.db'  # Replace with your SQLite database file path

    data_list = process_json_data(json_file_path)
    insert_to_sqlite(data_list, db_file)
