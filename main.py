from src.controllers.awards_data import *
from src.data.index_reformat_csv import index_in_csv
import json

with open('src\\config\\config.json', 'r') as f:
    config = json.load(f)
index_in_csv(config['database'])


server.run()
