import mysql.connector
import pandas as pd
from datetime import date

class database:
    def get_connection(self):
        database_connection = mysql.connector.connect(
            host="34.123.205.220",
            user="root",
            password="root",
            database = "academiclease"
        )
        return database_connection

    def init_db(self):
        database_connection = self.get_connection()
        cursor = database_connection.cursor()
        try:
            with open('schemas.sql', 'r') as f:
                x = f.read()
                print(x)
                cursor.execute(x,multi=True)
                database_connection.commit()
        except:
            print("failed")
            print(x)
            database_connection.rollback()
            database_connection.commit()
        database_connection.close()
        self.load_university()
    
    def load_university(self):
        df = pd.read_csv('us_universities.csv')
        arr = df.to_numpy()
        database_connection = self.get_connection()
        mycursor = database_connection.cursor()
        count=1
        for a in arr:
            a[0] =str(a[0]).replace("'"," ")
            query="insert into university_list values("+str(count)+",'"+str(a[0])+"','"+str(a[1])+"','"+str(date.today())+"');"
            count = count+1
            try:
                mycursor.execute(query)
                database_connection.commit()
            except:
                print("failed")
                print(query)
                database_connection.rollback()
                database_connection.commit()
        database_connection.close()


if __name__ == '__main__':
    obj = database()
    obj.init_db() 