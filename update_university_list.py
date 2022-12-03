import mysql.connector
import pandas as pd
database_connection = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Greeshma@123"
)
df = pd.read_csv('us_universities.csv')
arr = df.to_numpy()
mycursor = database_connection.cursor()
mycursor.execute("use cloud_project")
mycursor.execute("DROP table us_university_list;")
mycursor.execute("create table us_university_list(name varchar(100), url varchar(100));")
database_connection.commit()

for a in arr:
    a[0] =str(a[0]).replace("'"," ")
    query="insert into us_university_list values('"+str(a[0])+"','"+str(a[1])+"');"
    

    try:
        mycursor.execute(query)
        
        database_connection.commit()
    
    except:
        print("failed")
        print(query)
        
        database_connection.rollback()
        database_connection.commit()
 
database_connection.close()
