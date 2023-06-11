import os 
import logging
import pyodbc
from dotenv import load_dotenv


# Configure logging
logging.basicConfig(level= logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a class for utilities
class utilities_pyodbc:
    """
A utility class for working with pyodbc to connect to a SQL Server.

Args:
    server (str): The name or IP address of the SQL Server.
    database (str): The name of the database to connect to.
    port (str): The port number of the SQL Server.
    user (str): The username for the SQL Server authentication.
    password (str): The password for the SQL Server authentication.

Attributes:
    server (str): The name or IP address of the SQL Server.
    database (str): The name of the database to connect to.
    port (str): The port number of the SQL Server.
    user (str): The username for the SQL Server authentication.
    password (str): The password for the SQL Server authentication.

Methods:
    connectSqlServer: Connects to the SQL Server and returns the connection and cursor objects.

"""
    def __init__(self, server, database, port, user, password):
        self.server = server
        self.database = database
        self.port = port
        self.user = user
        self.password = password
        
    #check connection to SQL server
    def connectSqlServer(self):
        """
        Connects to the SQL Server using the provided connection parameters.

        Returns:
            tuple: A tuple containing a boolean indicating the connection status (True if successful, False otherwise),
            the connection object, and the cursor object.

        """
        try:
            conn = pyodbc.connect('Driver={SQL Server}; Server='+self.server+'; Database='+self.database+'; Port='+self.port+'; UID='+self.user+'; PWD='+self.password+';')
            cursor = conn.cursor()
            logging.info("Connected to SQL Server successfully!")
            return True,conn, cursor

        except Exception as e:
            logging.error("An error occurred when connecting to DB, error details: {}".format(e))
            return False, None, None
    
    