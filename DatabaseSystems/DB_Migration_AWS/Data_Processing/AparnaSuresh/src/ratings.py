import pandas as pd
import ast
import mysql.connector

df = pd.read_csv("C:/Users/aparn/OneDrive/Documents/SJSU/DATA_225/Lab/Lab_1/DATA225-Lab1-main/DATA225-Lab1/res/ratings_small.csv")

print(df.head())

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Aparna@9',
    database='TMDB'
)

print("Sucessfully connected to MySQL")

if connection.is_connected():
    cursor = connection.cursor()

    # Drop table if it exists
    drop_table_query = "DROP TABLE IF EXISTS ratings"
    cursor.execute(drop_table_query)
    print("Dropped table")

    print(df.dtypes)
    df['rating'] = df['rating'].astype(str)

    cursor.execute("CREATE TABLE ratings(user_id INT,movie_id INT, rating FLOAT, timestamp INT, PRIMARY KEY(user_id,movie_id))")
    print("Created table")
    for index, row in df.iterrows():
        insert_query = "INSERT INTO ratings (user_id, movie_id, rating, timestamp) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (row['userId'], row['movieId'], row['rating'], row['timestamp']))
    print("Inserted Data")

    # Commit changes and close cursor
    connection.commit()
    cursor.close()

if connection.is_connected():
    connection.close()
