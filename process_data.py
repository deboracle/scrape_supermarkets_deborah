# This code processes the raw data from the json files and inserts them to a table
# What we want to insert:
# description, nutrition itm (ingredients), symbole (sucar, shuman), unite de mesure, categorie, pct de fruits, marque, allergenes, may contain, image url

import sqlite3
import json