
################

import time
import requests
import csv
import pyodbc
import datetime
import os
import logging
from dotenv import load_dotenv
from Libs.RestaurantInspectionUtility import RestaurantInspectionUtility

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


###########################

#test exampple get data from API

# def get_restaurant_inspection_data(url):
#     response = requests.get(url)
    
#     if response.status_code == 200:
#         data = response.text
#         # Parse the response in csv data
#         reader = csv.DictReader(data.splitlines())
#         data = list(reader)
#         return data
#     else:
#         logging.error(f"Error occurred while retrieving data: {response.status_code}")
#         return None

# # URL for restaurant inspection data
# url_restaurant_inspection = 'https://data.cityofnewyork.us/api/views/43nn-pn8j/rows.csv'

# # Call the function to get the restaurant inspection data
# data_restaurant_inspection = get_restaurant_inspection_data(url_restaurant_inspection)

# # Check if data was successfully retrieved
# if data_restaurant_inspection:
#     logging.info("Data retrieved successfully!")
# else:
#     logging.error("Failed to retrieve data.")
    
#####################
#add current time to print status
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#get full data from API

logging.info("The process get API data is starting...")

utility_restaurant = RestaurantInspectionUtility('https://data.cityofnewyork.us/api/views/43nn-pn8j/rows.csv')

data_restaurant_inspection = utility_restaurant.get_restaurant_inspection_data()


# def retrieve_all_restaurant_inspection_data():
#     url_restaurant_inspection = 'https://data.cityofnewyork.us/api/views/43nn-pn8j/rows.csv'
#     # limit = 1000  # Number of records to retrieve per request
#     # offset = 0  # Initial offset

#     # data_restaurant_inspection = []

#     # Make the API request
#     response = requests.get(url_restaurant_inspection)

#     # Check if the request was successful
#     if response.status_code == 200:
#         # Parse the csv data from the response
#         data = response.text
#         reader = csv.DictReader(data.splitlines())
#         all_data_restaurant_inspection = list(reader)
#         logging.info(f"Data has been retrieval, status: {len(all_data_restaurant_inspection)}")
        
#         # Check if there are more records to retrieve
#     #     if len(data) < limit:
#     #         logging.info('Data retrieval completed.')
#     #         break  # All data has been retrieved
#     #     else:
#     #         offset += limit  # Move to the next batch
#     else:
#         logging.error('Error occurred while retrieving data:', response.status_code)
#         break

#     return all_data_restaurant_inspection

# Usage:
# data_restaurant_inspection = retrieve_all_restaurant_inspection_data()

#create the folder structure base on current date
def save_file_as_structure(dataset):
    #get current date
    current_date = datetime.datetime.now()
    #create folder structure
    year_folder = current_date.strftime("%Y")
    month_folder = current_date.strftime("%m")
    day_folder = current_date.strftime("%d")
    folder_structure = "restaurant_inspection_data"+ "/"+year_folder + "/" + month_folder + "/" + day_folder
    os.makedirs(folder_structure, exist_ok=True)
    
    #save the retrieved data to a json file
    restaurant_inspection_file_path = folder_structure + "/" + current_date.strftime("%Y_%m_%d_%H_%M") + "_restaurant_inspection.csv"
    with open(restaurant_inspection_file_path, 'w', newline= "", encoding= 'utf-8') as file:
        write = csv.writer(file)
        write.writerow(dataset[0].keys())
        write.writerows(map(lambda x: x.values(), dataset))
    logging.info(f"Data has been saved to file: {restaurant_inspection_file_path}")
    return restaurant_inspection_file_path
 
 #save all restaurant inspection data to a csv in local machine   
# save_file_as_structure(data_restaurant_inspection)

# the path csv file was stored in local machine
csv_restaurant_inspection_file_path = save_file_as_structure(data_restaurant_inspection)

#covert the file path to window format
csv_restaurant_inspection_file_path = os.path.abspath(csv_restaurant_inspection_file_path)

# Check if the file exists
if os.path.exists(csv_restaurant_inspection_file_path):
    # Open the file
    with open(csv_restaurant_inspection_file_path, newline='', encoding='utf-8') as file:
        dict_restaurant_inspection = csv.DictReader(file)
else:
    print("File does not exist:", csv_restaurant_inspection_file_path)

#check connection to SQL server
def connectSqlServer(Server, Database, Port, User, Password):
    try:
        conn = pyodbc.connect('Driver={SQL Server}; Server='+Server+'; Database='+Database+'; Port='+Port+'; UID='+User+'; PWD='+Password+';')
        cursor = conn.cursor()
        logging.info("Connected to SQL Server successfully!")
        return True,conn, cursor

    except Exception as e:
        print("An error occurred when connecting to DB, error details: {}".format(e))
        return False, None, None

# Define your server, database, port, username, and password
load_dotenv(".env")
server = os.getenv("SERVER_NAME")
database = os.getenv("DWH_Staging")
port = os.getenv("PORT_SQLSERVER")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

# Connect to the SQL Server
success,conn,cursor = connectSqlServer(server, database, port, username, password)


if success:
    try:
        logging.info("Truncating the table...")
        cursor.execute("TRUNCATE TALBE dbo.raw_restaurant_inspection")
        #open the local csv file
        with open(csv_restaurant_inspection_file_path, 'r', encoding='utf-8', newline='') as csvfile:
             # Create a CSV reader object
            reader = csv.DictReader(csvfile)
        # Iterate over each row in the CSV file
            logging.info("Inserting data into the table...")
            for row in reader:
                # Extract the values from the row
                camis = row['CAMIS'].replace("'", "''")
                dba = row['DBA'].replace("'", "''")
                boro = row['BORO'].replace("'", "''")
                building = row['BUILDING'].replace("'", "''")
                street = row['STREET'].replace("'", "''")
                zipcode = row['ZIPCODE'].replace("'", "''")
                phone = row['PHONE'].replace("'", "''")
                cuisine_description = row['CUISINE DESCRIPTION'].replace("'", "''")
                inspection_date = row['INSPECTION DATE'].replace("'", "''")
                action = row['ACTION'].replace("'", "''")
                violation_code = row['VIOLATION CODE'].replace("'", "''")
                violation_desc = row['VIOLATION DESCRIPTION'].replace("'", "''")
                critical_flag = row['CRITICAL FLAG'].replace("'", "''")
                score = row['SCORE'].replace("'", "''")
                grade = row['GRADE'].replace("'", "''")
                grade_date = row['GRADE DATE'].replace("'", "''")
                record_date = row['RECORD DATE'].replace("'", "''")
                inspection_type = row['INSPECTION TYPE'].replace("'", "''")
                latitude = row['Latitude'].replace("'", "''")
                longitude = row['Longitude'].replace("'", "''")
                community_board = row['Community Board'].replace("'", "''")
                council_district = row['Council District'].replace("'", "''")
                census_tract = row['Census Tract'].replace("'", "''")
                bin_number = row['BIN'].replace("'", "''")
                bbl_number = row['BBL'].replace("'", "''")
                nta = row['NTA'].replace("'", "''")
                # try:
                #     encoded_camis = camis.encode('utf-8', errors='ignore')
                #     encoded_dba = dba.encode('utf-8', errors='ignore')
                # except UnicodeEncodeError:
                #     # Handle or log the error as needed
                #     continue
                # Generate the SQL INSERT statement
                sql = f"INSERT INTO dbo.raw_restaurant_inspection (camis, dba, boro, building, street, zipcode, phone, cuisine, inspection_date, action, violation_code, violation_desc, critical_flag, score, grade, grade_date, record_date, inspection_type, latitude, longitude, community_board, council_district, census_tract, bin_number, bbl_number, nta) VALUES ('{camis}', '{dba}', '{boro}', '{building}', '{street}', '{zipcode}', '{phone}', '{cuisine_description}', '{inspection_date}', '{action}', '{violation_code}', '{violation_desc}', '{critical_flag}', '{score}', '{grade}', '{grade_date}', '{record_date}', '{inspection_type}', '{latitude}', '{longitude}', '{community_board}', '{council_district}', '{census_tract}', '{bin_number}', '{bbl_number}', '{nta}')"
                # Execute the insert query
                cursor.execute(sql)
                # Print the status of the row insertion
                #logging.info(f"Row inserted successfully: {row}")
                # pause execution for 10 second
                # time.sleep(0.01)
                # Commit the changes to the database
                cursor.commit()
            

    except Exception as e:
        logging.error(f"An error occurred when truncating or inserting data into the table, error details: {e}")

    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()
        # Close the file after processing
        csvfile.close()
        logging.info(f"All data was inserted successfully")
else:
    logging.error("Failed to connect to the SQL Server.")