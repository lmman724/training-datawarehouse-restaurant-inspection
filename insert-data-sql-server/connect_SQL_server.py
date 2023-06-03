
######
import requests
import csv

csv_restaurant_inspection_link = "https://data.cityofnewyork.us/resource/43nn-pn8j.csv"  

#dowload csv file
response = requests.get(csv_restaurant_inspection_link)
content = response.content.decode('utf-8')
# Read the CSV content as a string
csv_content = csv.reader(content.splitlines())
    
# Convert CSV content into a list of dictionaries
data = []
header = None
for row in csv_content:
    if header is None:
        header = row
    else:
        data.append(dict(zip(header, row)))
    
    # Iterate over each row in the CSV file
    for row in data:
        # Extract the values from the row
        camis = row['camis']
        dba = row['dba']
        boro = row['boro']
        building = row['building']
        street = row['street']
        zipcode = row['zipcode']
        phone = row['phone']
        cuisine = row['cuisine_description']
        inspection_date = row['inspection_date']
        action = row['action']
        violation_code = row['violation_code']
        violation_desc = row['violation_description']
        critical_flag = row['critical_flag']
        score = row['score']
        grade = row['grade']
        grade_date = row['grade_date']
        record_date = row['grade_date']
        inspection_type = row['inspection_type']
        latitude = row['latitude']
        longitude = row['longitude']
        community_board = row['community_board']
        council_district = row['council_district']
        census_tract = row['census_tract']
        bin_number = row['bin']
        bbl_number = row['bbl']
        nta = row['nta']
        # try:
        #     encoded_camis = camis.encode('utf-8', errors='ignore')
        #     encoded_dba = dba.encode('utf-8', errors='ignore')
        # except UnicodeEncodeError:
        #     # Handle or log the error as needed
        #     continue
        # Generate the SQL INSERT statement
        sql = f"INSERT INTO dbo.food_inspection (CAMIS, DBA, BORO, BUILDING, STREET, ZIPCODE, PHONE, CUISINE, INSPECTION_DATE, ACTION, VIOLATION_CODE, VIOLATION_DESC, CRITICAL_FLAG, SCORE, GRADE, GRADE_DATE, RECORD_DATE, INSPECTION_TYPE, LATITUDE, LONGITUDE, COMMUNITY_BOARD, COUNCIL_DISTRICT, CENSUS_TRACT, BIN_NUMBER, BBL_NUMBER, NTA) VALUES ('{camis}', '{dba}', '{boro}', '{building}', '{street}', '{zipcode}', '{phone}', '{cuisine}', '{inspection_date}', '{action}', '{violation_code}', '{violation_desc}', '{critical_flag}', '{score}', '{grade}', '{grade_date}', '{record_date}', '{inspection_type}', '{latitude}', '{longitude}', '{community_board}', '{council_district}', '{census_tract}', '{bin_number}', '{bbl_number}', '{nta}')"
        
        # Print the SQL statement or write it to a file as per your requirement
        print(sql.encode("utf-8"))

################

import time
import requests
import csv
import pyodbc
import datetime

#add current time to print status
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def connectSqlServer(Server, Database, Port, User, Password):
    try:
        conn = pyodbc.connect('Driver={SQL Server}; Server='+Server+'; Database='+Database+'; Port='+Port+'; UID='+User+'; PWD='+Password+';')
        cursor = conn.cursor()
        return True,conn, cursor

    except Exception as e:
        print("An error occurred when connecting to DB, error details: {}".format(e))
        return False, None

# Define your server, database, port, username, and password
server = '127.0.0.1'
database = 'DWH_Staging'
port = "1433"
username = 'lmman'
password = 'Ngoan03688@'

# Connect to the SQL Server
success,conn,cursor = connectSqlServer(server, database, port, username, password)

if success:
    try:
        csv_restaurant_inspection_link = "https://data.cityofnewyork.us/resource/43nn-pn8j.csv"  

        #dowload csv file
        response = requests.get(csv_restaurant_inspection_link)
        content = response.content.decode('utf-8')
        # Read the CSV content as a string
        csv_content = csv.reader(content.splitlines())
            
        # Convert CSV content into a list of dictionaries
        data = []
        header = None
        for row in csv_content:
            if header is None:
                header = row
            else:
                data.append(dict(zip(header, row)))
    
        # Iterate over each row in the CSV file
        for row in data:
            # Extract the values from the row
            camis = row['camis'].replace("'", "''")
            dba = row['dba'].replace("'", "''")
            boro = row['boro'].replace("'", "''")
            building = row['building'].replace("'", "''")
            street = row['street'].replace("'", "''")
            zipcode = row['zipcode'].replace("'", "''")
            phone = row['phone'].replace("'", "''")
            cuisine = row['cuisine_description'].replace("'", "''")
            inspection_date = row['inspection_date'].replace("'", "''")
            action = row['action'].replace("'", "''")
            violation_code = row['violation_code'].replace("'", "''")
            violation_desc = row['violation_description'].replace("'", "''")
            critical_flag = row['critical_flag'].replace("'", "''")
            score = row['score'].replace("'", "''")
            grade = row['grade'].replace("'", "''")
            grade_date = row['grade_date'].replace("'", "''")
            record_date = row['grade_date'].replace("'", "''")
            inspection_type = row['inspection_type'].replace("'", "''")
            latitude = row['latitude'].replace("'", "''")
            longitude = row['longitude'].replace("'", "''")
            community_board = row['community_board'].replace("'", "''")
            council_district = row['council_district'].replace("'", "''")
            census_tract = row['census_tract'].replace("'", "''")
            bin_number = row['bin'].replace("'", "''")
            bbl_number = row['bbl'].replace("'", "''")
            nta = row['nta'].replace("'", "''")
            # try:
            #     encoded_camis = camis.encode('utf-8', errors='ignore')
            #     encoded_dba = dba.encode('utf-8', errors='ignore')
            # except UnicodeEncodeError:
            #     # Handle or log the error as needed
            #     continue
            # Generate the SQL INSERT statement
            sql = f"INSERT INTO dbo.restaurant_inspection (camis, dba, boro, building, street, zipcode, phone, cuisine, inspection_date, action, violation_code, violation_desc, critical_flag, score, grade, grade_date, record_date, inspection_type, latitude, longitude, community_board, council_district, census_tract, bin_number, bbl_number, nta) VALUES ('{camis}', '{dba}', '{boro}', '{building}', '{street}', '{zipcode}', '{phone}', '{cuisine}', '{inspection_date}', '{action}', '{violation_code}', '{violation_desc}', '{critical_flag}', '{score}', '{grade}', '{grade_date}', '{record_date}', '{inspection_type}', '{latitude}', '{longitude}', '{community_board}', '{council_district}', '{census_tract}', '{bin_number}', '{bbl_number}', '{nta}')"
            # Execute the insert query
            cursor.execute(sql)
            # Print the status of the row insertion
            print(f"{current_time} - Row inserted successfully:", row)
            # pause execution for 10 second
            time.sleep(0.01)
        # Commit the changes to the database
        cursor.commit()

    except Exception as e:
        print("An error occurred when inserting data into the table, error details: {},\n{}".format(e,sql))

    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()
else:
    print("Failed to connect to the SQL Server.")
