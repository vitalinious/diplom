import customtkinter as cstk
import pypyodbc as pyodbc
import tkinter
from datetime import datetime

# Параметры подключения
DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'VITSIRYK-LAPTOP'
DATABSE_NAME = 'TestDb'

connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABSE_NAME};
    Trust_Connection=yes;
"""

def create_users_table():
    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE Users (
                userID INT IDENTITY(1,1) PRIMARY KEY,
                username NVARCHAR(25) NOT NULL UNIQUE,
                password NVARCHAR(25) NOT NULL,
                registration_date DATE NOT NULL,
                registration_time DATETIME NOT NULL
            )
        """)
        connection.commit()
        print("Users table created successfully")
    except pyodbc.Error as ex:
        print("Error creating table:", ex)
    finally:
        if 'connection' in locals():
            connection.close()
            
create_users_table()