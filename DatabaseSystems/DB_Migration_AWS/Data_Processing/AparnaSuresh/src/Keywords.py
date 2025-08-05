import pandas as pd
import ast
import mysql.connector

df = pd.read_csv("C:/Users/aparn/OneDrive/Documents/SJSU/DATA_225/Lab/Lab_1/DATA225-Lab1-main/DATA225-Lab1/res/keywords.csv")

df['keywords'] = df['keywords'].apply(ast.literal_eval)
keywords = pd.DataFrame(columns=['id','name'])
# Create an empty list to store the 'id' and 'name' values
id_list = []
name_list = []

for dictionary in df['keywords']:
    for dict_entry in dictionary:
        if 'id' in dict_entry:
            id_list.append(dict_entry['id'])
        if 'name' in dict_entry:
            name_list.append(dict_entry['name'])

keywords['id'] = id_list
keywords['name'] = name_list
keywords['name'] = keywords['name'].astype(str)

print(keywords.dtypes)


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
    drop_table_query = "DROP TABLE IF EXISTS keywords"
    cursor.execute(drop_table_query)
    print("Dropped table")

    cursor.execute("CREATE TABLE keywords(keyword_id INT PRIMARY KEY,keyword_name VARCHAR(200))")
    print("Created table")

    # Remove duplicates
    keywords.drop_duplicates(subset=['id'], keep='first', inplace=True)
    #keywords.drop_duplicates(subset=['name'], keep='first', inplace=True)

    insert_query=("INSERT INTO keywords(keyword_id,keyword_name) VALUES (%s,%s)")
    for index, row in keywords.iterrows():
        cursor.execute(insert_query, (row['id'], row['name']))
    print("Inserted Data")

    # Commit changes and close cursor
    connection.commit()
    cursor.close()

if connection.is_connected():
    connection.close()