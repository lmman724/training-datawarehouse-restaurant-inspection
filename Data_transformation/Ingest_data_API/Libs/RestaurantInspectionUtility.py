import os
import datetime
import logging
import requests
import csv
import pyodbc
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class RestaurantInspectionUtility:
    def __init__(self, url_restaurant_inspection):
        self.url_restaurant_inspection = url_restaurant_inspection
        
    def get_restaurant_inspection_data(self):
        response = requests.get(self.url_restaurant_inspection)
        
        if response.status_code == 200:
            data = response.text
            # Parse the response in csv data
            reader = csv.DictReader(data.splitlines())
            data = list(reader)
            logging.info(f"Data has been retrieval, status: {len(data)}")
        else:
            logging.error(f"Error occurred while retrieving data: {response.status_code}")
        return data