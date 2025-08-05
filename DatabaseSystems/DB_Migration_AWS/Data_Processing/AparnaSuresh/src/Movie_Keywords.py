import pandas as pd
import ast
import mysql.connector

df = pd.read_csv("C:/Users/aparn/OneDrive/Documents/SJSU/DATA_225/Lab/Lab_1/DATA225-Lab1-main/DATA225-Lab1/res/keywords.csv")

df['keywords'] = df['keywords'].apply(ast.literal_eval)
movie_Keywords = pd.DataFrame(columns=['id','tmdb_id'])
id_list = []
tmdbid_list=[]
index = 0

for dictionary in df['keywords']:
    for dict_entry in dictionary:
        #for key,value in dict_entry.items():
            #print(df['id'][index],key,value)
        tmdbid_list.append(df['id'][index])
        if 'id' in dict_entry:
            id_list.append(dict_entry['id'])
    index += 1

movie_Keywords['id'] = id_list
movie_Keywords['tmdb_id'] = tmdbid_list

print(movie_Keywords.dtypes)


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
    drop_table_query = "DROP TABLE IF EXISTS movie_keywords"
    cursor.execute(drop_table_query)
    print("Dropped table")

    cursor.execute("CREATE TABLE movie_keywords(keyword_id INT,tmdb_id INT, FOREIGN KEY (keyword_id) REFERENCES keywords(keyword_id))")
    print("Created table")
    insert_query=("INSERT INTO movie_keywords(keyword_id,tmdb_id) VALUES (%s,%s)")
    for index, row in movie_Keywords.iterrows():
        id_value = int(row['id'])
        tmdb_id_value = int(row['tmdb_id'])
        cursor.execute(insert_query, (id_value, tmdb_id_value))
    print("Inserted Data")

    # Commit changes and close cursor
    connection.commit()
    cursor.close()

if connection.is_connected():
    connection.close()
