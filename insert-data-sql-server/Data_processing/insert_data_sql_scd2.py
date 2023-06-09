import csv
import logging
import pyodbc
import time

# Open a connection to the database
connection = pyodbc.connect('<your_connection_string_here>')
cursor = connection.cursor()

# Path to the CSV file
csv_restaurant_inspection_file_path = 'restaurant_inspection_data.csv'

try:
    # Open the local CSV file
    with open(csv_restaurant_inspection_file_path, 'r', encoding='utf-8', newline='') as csvfile:
        # Create a CSV reader object
        reader = csv.DictReader(csvfile)
        
        # Create a set to store the unique CAMIS values
        existing_camis = set()
        
        # Retrieve existing CAMIS values from the database
        cursor.execute("SELECT DISTINCT camis FROM dbo.raw_restaurant_inspection")
        for row in cursor.fetchall():
            existing_camis.add(row[0])
        
        # Iterate over each row in the CSV file
        logging.info("Inserting data into the table...")
        for row in reader:
            # Extract the values from the row
            camis = row['CAMIS'].replace("'", "''")
            
            # Check if the CAMIS value is already present in the database
            if camis in existing_camis:
                # Perform SCD Type 2 update
                
                # Set the end date of the previous record to the current date
                update_sql = f"UPDATE dbo.raw_restaurant_inspection SET end_date = GETDATE() WHERE camis = '{camis}' AND end_date IS NULL"
                cursor.execute(update_sql)
                
                # Generate the SQL INSERT statement for the new record
                sql = f"INSERT INTO dbo.raw_restaurant_inspection (camis, dba, boro, building, street, zipcode, phone, cuisine, inspection_date, action, violation_code, violation_desc, critical_flag, score, grade, grade_date, record_date, inspection_type, latitude, longitude, community_board, council_district, census_tract, bin_number, bbl_number, nta, start_date, end_date) VALUES ('{camis}', '{dba}', '{boro}', '{building}', '{street}', '{zipcode}', '{phone}', '{cuisine_description}', '{inspection_date}', '{action}', '{violation_code}', '{violation_desc}', '{critical_flag}', '{score}', '{grade}', '{grade_date}', '{record_date}', '{inspection_type}', '{latitude}', '{longitude}', '{community_board}', '{council_district}', '{census_tract}', '{bin_number}', '{bbl_number}', '{nta}', GETDATE(), NULL)"
                cursor.execute(sql)
                
                logging.info(f"Updated record for CAMIS: {camis}")
            else:
                # Insert a new record
                
                # Generate the SQL INSERT statement
                sql = f"INSERT INTO dbo.raw_restaurant_inspection (camis, dba, boro, building, street, zipcode, phone, cuisine, inspection_date, action, violation_code, violation_desc, critical_flag, score, grade, grade_date, record_date, inspection_type, latitude, longitude, community_board, council_district, census_tract, bin_number, bbl_number, nta, start_date, end_date) VALUES ('{camis}', '{dba}', '{boro}', '{building}', '{street}', '{zipcode}', '{phone}', '{cuisine_description}', '{inspection_date}', '{action}', '{violation_code}', '{violation_desc}', '{critical_flag}', '{score}', '{grade}', '{grade_date}', '{record_date}', '{inspection_type}', '{latitude}', '{longitude}', '{community_board}', '{council_district}', '{census_tract}', '{bin_number}', '{bbl_number}', '{nta}', GETDATE(), NULL)"
                cursor.execute(sql)
                
                # Add the new CAMIS value to the existing_camis set
                existing_camis.add(camis)
                
                logging.info(f"Inserted new record for CAMIS: {camis}")
            
        # Commit the changes to the database
        cursor.commit()

except Exception as e:
    logging.error(f"An error occurred when inserting data into the table, error details: {e}")

finally:
    # Close the cursor and connection
    cursor.close()
    connection.close()
    
    # Close the file after processing
    csvfile.close()
    
    logging.info("All data was inserted successfully")
