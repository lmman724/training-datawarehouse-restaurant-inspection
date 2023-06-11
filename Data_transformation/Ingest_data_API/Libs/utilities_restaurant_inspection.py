import os
import datetime
import logging
import requests
import csv

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class restaurant_inspection:
    def __init__(self, url_restaurant_inspection, output_folder):
        self.url_restaurant_inspection = url_restaurant_inspection
        self.output_folder = output_folder
        
    def get_restaurant_inspection_data(self):
        """Retrieve restaurant inspection data from the specified URL.
        
        Returns the parsed data as a list of dictionaries representing the CSV rows.
        If an error occurs during the data retrieval, None is returned.
        
        Returns:
            list[dict] or None: The retrieved restaurant inspection data as a list
            of dictionaries, or None if an error occurs.
        """
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
    
    def save_file_as_structure(self, dataset):
        """Create the folder structure based on the current date and save the retrieved data to a CSV file.

    Args:
        dataset (list): The list of dictionaries representing the retrieved data.

    Returns:
        str: The file path where the data has been saved.

    """
        current_date = datetime.datetime.now()
        year_folder = current_date.strftime("%Y")
        month_folder = current_date.strftime("%m")
        day_folder = current_date.strftime("%d")
        folder_structure = f"{self.output_folder}/{year_folder}/{month_folder}/{day_folder}"
        os.makedirs(folder_structure, exist_ok=True)
        
        restaurant_inspection_file_path = f"{folder_structure}/{current_date.strftime('%Y_%m_%d_%H_%M')}_restaurant_inspection.csv"
        try:
            with open(restaurant_inspection_file_path, 'w', newline="", encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(dataset[0].keys())
                writer.writerows(map(lambda x: x.values(), dataset))
            logging.info(f"Data has been saved to file: {restaurant_inspection_file_path}")
            return os.path.abspath(restaurant_inspection_file_path)
        except Exception as e:
            logging.error(f"Error occurred while saving data to file: {e}")
            raise