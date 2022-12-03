import mysql.connector
import pandas as pd
database_connection = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Greeshma@123"
)
df = pd.read_csv('us_universities.csv')
mycursor = database_connection.cursor()