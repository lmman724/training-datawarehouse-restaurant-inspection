from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
import logging
import datetime


# Config logging

logging.basicConfig(format= "%(asctime)s - %(levelname)s - %(message)s", level= logging.INFO)

#################
def establish_connection(username, password, server_name,port, database_name):
    # Create the connection string
    #connection_string = f'mssql+pyodbc://{username}:{password}@{server_name}/{database_name}?driver=ODBC+Driver+17+for+SQL+Server'
    connection_string = f"mssql+pyodbc://{username}:{password}@{server_name}:{port}/{database_name}?driver=ODBC+Driver+17+for+SQL+Server"

    try:
        # Establish a connection to the SQL Server database using SQLAlchemy
        engine = create_engine(connection_string)
        Session = sessionmaker(bind=engine)
        session = Session()

        # Log the successful connection
        logging.info('Connection to the SQL Server database established successfully.')
        
        return session

    except Exception as e:
        logging.error(f'Error occurred while establishing the connection: {e}')
        return None

# Usage
username = 'lmman'
password = '12345678x@X'
server_name = '127.0.0.1'
database_name = 'DWH_Staging'
port = "1433"
#driver = "mssql+pyodbc"

# Establish the connection
session = establish_connection(username, password, server_name,port, database_name)


##################


# Define the SQLAlchemy model for DimRestaurantPlaces table
Base = declarative_base()

class DimRestaurantPlaces(Base):
    __tablename__ = 'DimRestaurantPlaces'

    restaurant_key = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer)
    restaurant_name = Column(String(200))
    phone = Column(String(15))
    

# Check if the connection was successful
if session is not None:
    # Perform your operations using the session
    stage_data = session.execute(text("SELECT TOP(10) * FROM dbo.restaurant_inspection")).fetchall()
    # Close the session when done
    session.close()
    logging.info("Operations completed sucessfully.")
else:
    # Handle connection failure
    logging.error("Connection to the SQL server failed")

# Fetch data from the stage table

# stage_data = session.execute(text("SELECT TOP(10) * FROM dbo.restaurant_inspection")).fetchall()

# Transform and load data into DimRestaurantPlaces table
for row in stage_data:
    # Perform transformations and mappings
    restaurant_id = row.camis
    restaurant_name = row.dba
    phone = row.phone

    # Create a new instance of DimRestaurantPlaces
    dim_restaurant = DimRestaurantPlaces(restaurant_id=restaurant_id, restaurant_name=restaurant_name, phone=phone)
    
    # Add the instance to the session
    session.add(dim_restaurant)

# Commit the changes to the database
session.commit()

# Close the session
session.close()
