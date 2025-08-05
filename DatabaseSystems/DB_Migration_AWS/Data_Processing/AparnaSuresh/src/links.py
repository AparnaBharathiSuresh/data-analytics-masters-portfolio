import pandas as pd
import ast
import mysql.connector

df = pd.read_csv("C:/Users/aparn/OneDrive/Documents/SJSU/DATA_225/Lab/Lab_1/DATA225-Lab1-main/DATA225-Lab1/res/links.csv")

df.dropna(inplace=True)

df.reset_index(drop=True, inplace=True)
print(df.dtypes)

print(df.head())

df['tmdbId'] = df['tmdbId'].astype(int)

print(df.dtypes)

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
    drop_table_query = "DROP TABLE IF EXISTS links"
    cursor.execute(drop_table_query)
    print("Dropped table")
    #cursor.execute("DROP INDEX movie_id_index ON ratings")
    cursor.execute("CREATE INDEX movie_id_index ON ratings (movie_id)")
    cursor.execute("CREATE TABLE links(movie_id INT,imdb_id INT,tmdb_id INT)")
    print("Created table")
    for index, row in df.iterrows():
        insert_query = "INSERT INTO links (movie_id, imdb_id, tmdb_id) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (int(row['movieId']), int(row['imdbId']), int(row['tmdbId'])))
    print("Inserted Data")

    # Commit changes and close cursor
    connection.commit()
    cursor.close()

if connection.is_connected():
    connection.close()

