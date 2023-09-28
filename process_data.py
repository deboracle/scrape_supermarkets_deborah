# This code processes the raw data from the json files and inserts them to a table
# TODO: check if key exists, if not return null

import sqlite3
import json


def check_key(data, keys):
    # This function returns None if the key doesnt exist
    current_key = keys[0]

    if current_key in data:
        if len(keys) == 1:
            return data[current_key]
        else:
            return check_key(data[current_key], keys[1:])
    else:
        return None


def process_json_data(json_file_path):
    data_list = []

    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

        # This helper function will return None if a key is not found in the JSON
        # TODO: try to find symbol, fruit pct
        # TODO: nutrition values & categories fix


        for item in data:
            product_data = {}
            product_data['barcode'] = check_key(item, ['barcode'])
            product_data['ingredients'] = check_key(item, ['data', '1', 'ingredients'])
            product_data['unit_of_measure'] = check_key(item, ['unitOfMeasure', 'defaultName']) #we can change it to id
            product_data['brand'] = check_key(item, ['brand', 'names', '2'])
            product_data['allergens'] = check_key(item, ['data', '1', 'containAllergens'])
            product_data['might_contain'] = check_key(item, ['data', '1', 'mightContainAllergens'])
            product_data['image_url'] = check_key(item, ['image', 'url'])
            product_data['name_he'] = check_key(item, ['names', '1', 'short'])
            product_data['name_en'] = check_key(item, ['names', '2', 'short'])

            print(product_data)

            # Extract all categories for product
            categories_list = []
            for categories in check_key(item, ['family', 'categories']):
                categories_list.append([categories['names']['2'], categories['names']['1']])

            # same for nutrition values
            # nutr_values = item['nutritionValues']

            data_list.append(product_data)
            print(product_data)

    return data_list


# Define a function to insert data into an SQLite database
def insert_to_sqlite(data_list, db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # TODO: Nutrition values, Fruit Pct.
    # Create a table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                        Description TEXT NOT NULL,
                        ItemCode int NOT NULL,
                        Ingredients TEXT,
                        UnitOfMeasure TEXT,
                        Categories TEXT,
                        Brand TEXT,
                        Allergens TEXT,
                        MightContain TEXT,
                        ImageUrl TEXT,
                        PRIMARY KEY(ItemCode)
                    )''')

    # Insert data into the table
    for product_data in data_list:
        cursor.execute('''INSERT INTO products (description, ItemCode, Ingredients, UnitOfMeasure, Category, 
                        Brand, Allergens, MightContain, ImageUrl) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                       (product_data['description'], product_data['barcode'], product_data['ingredients'],
                        product_data['unit_of_measure'], product_data['categories'], product_data['brand'],
                        product_data['allergens'], product_data['might_contain'], product_data['image_url']))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    json_file_path = './mck_data.json'
    db_file = '/Users/deborahgironde/Downloads/deborah_data.db'  # Replace with your SQLite database file path

    data_list = process_json_data(json_file_path)
    insert_to_sqlite(data_list, db_file)
