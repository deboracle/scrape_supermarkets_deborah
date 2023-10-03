# this is just to get all of the categories and ids
import json
import pandas as pd
import xlsxwriter


def get_ids():
    # Replace 'your_large_file.json' with the path to your large JSON file
    input_file_path = './mck_data.json'

    # Initialize an empty set to store unique categories
    unique_categories_id = set()

    # Read and process the JSON file
    with open(input_file_path, 'r') as json_file:
        category_ids = {}
        data = json.load(json_file)
        for item in data:
            # Initialize an empty list to store category IDs
            try:
                # Extract the 'id' from each category path and append to the list
                for categories in item['family']['categories']:
                    print(categories)
                    id = categories['id']
                    name_en = categories['names']['2']
                    name_he = categories['names']['1']
                    print(id, name_en, name_he)
                    if id not in category_ids:
                        category_ids[name_en] = name_he
                    else:
                        pass
            except KeyError:
                try:
                    if item['department']['id'] not in category_ids:
                        category_ids[item['department']['id']] = item['department']['name']
                except KeyError:
                    pass

    # Print the list of unique categories
    return category_ids


def insert_to_table(data):
    # inserts to excel file
    print(data)
    df = pd.DataFrame(data=data, index=[0])
    df = (df.T)
    print(df)
    df.to_excel('categories.xlsx')

insert_to_table(get_ids())