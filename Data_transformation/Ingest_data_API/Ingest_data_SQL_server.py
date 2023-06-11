import csv
import os
import logging
from dotenv import load_dotenv
from Libs.utilities_restaurant_inspection import restaurant_inspection
from Libs.utilities_pyodbc import utilities_pyodbc

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Define your server, database, port, username, and password
load_dotenv(".env")
server = os.getenv("LOCALHOST")
dwh_staging = os.getenv("DWH_Staging")
port = os.getenv("PORT_SQLSERVER")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")


#####################

# create an instance for restaurant inspection utility class

utilities_restaurant = restaurant_inspection('https://data.cityofnewyork.us/api/views/43nn-pn8j/rows.csv', "restaurant_inspection_data")




# Retrieve restaurant inspection data from the specified URL.

logging.info("The process get API data is starting...")

data_restaurant_inspection = utilities_restaurant.get_restaurant_inspection_data()

#check if the data was retrieved successfully
if data_restaurant_inspection is not None:
    #save the retrieved data to the specified folder structure
    file_path = utilities_restaurant.save_file_as_structure(data_restaurant_inspection)

# Create an instance for utililies pyodbc class
utilities_sql = utilities_pyodbc(server, dwh_staging, port, username, password)

# Connect to the SQL Server
success,conn,cursor = utilities_sql.connectSqlServer()

###########################


if success:
    try:
        logging.info("Truncating the table...")
        cursor.execute("TRUNCATE TABLE dbo.raw_restaurant_inspection")
        #open the local csv file
        with open(file_path, 'r', encoding='utf-8', newline='') as csvfile:
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
        # Close the file after processing
        csvfile.close()
        
        # Close the cursor and connection
        cursor.close()
        conn.close()
        
        logging.info(f"All data was inserted successfully")
else:
    logging.error("Failed to connect to the SQL Server.")