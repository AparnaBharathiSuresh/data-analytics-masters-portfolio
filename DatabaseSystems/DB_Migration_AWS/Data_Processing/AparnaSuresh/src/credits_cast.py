import pandas as pd
import ast
import mysql.connector

df = pd.read_csv("C:/Users/aparn/OneDrive/Documents/SJSU/DATA_225/Lab/Lab_1/DATA225-Lab1-main/DATA225-Lab1/res/credits.csv")
credits_cast = pd.DataFrame(columns=['cast_id','character','credit_id','gender','id','name','order','profile_path','movie_id'])

df['cast'] = df['cast'].apply(ast.literal_eval)


castid_list = []
character_list = []
creditid_list=[]
gender_list=[]
id_list=[]
name_list=[]
order_list=[]
profilepath_list=[]

for dictionary in df['cast']:
    for dict_entry in dictionary:
        if 'cast_id' in dict_entry:
            castid_list.append(dict_entry['cast_id'])
        if 'character' in dict_entry:
            character_list.append(dict_entry['character'])
        if 'credit_id' in dict_entry:
            creditid_list.append(dict_entry['credit_id'])
        if 'gender' in dict_entry:
            gender_list.append(dict_entry['gender'])
        if 'id' in dict_entry:
            id_list.append(dict_entry['id'])
        if 'name' in dict_entry:
            name_list.append(dict_entry['name'])
        if 'order' in dict_entry:
            order_list.append(dict_entry['order'])
        if 'profile_path' in dict_entry:
            profilepath_list.append(dict_entry['profile_path'])

credits_cast['cast_id'] = castid_list
credits_cast['character'] = character_list
#credits_cast['character'] = credits['character'].astype(str)
credits_cast['credit_id'] = creditid_list
credits_cast['gender'] = gender_list
credits_cast['id'] = id_list
credits_cast['name'] = name_list
#credits_cast['name'] = credits['name'].astype(str)
credits_cast['order'] = order_list
credits_cast['profile_path'] = profilepath_list
credits_cast['movie_id']=df['id']
#credits_cast['profile_path'] = credits['profile_path'].astype(str)



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
    drop_table_query = "DROP TABLE IF EXISTS credits_cast"
    cursor.execute(drop_table_query)
    print("Dropped table")

    cursor.execute("CREATE TABLE credits_cast(cast_id INT PRIMARY KEY,`character` VARCHAR(200),credit_id VARCHAR(200),gender INT,id INT,`name` VARCHAR(200),`order` INT,profile_path VARCHAR(200),movie_id INT)")
    print("Created table")

    credits_cast.drop_duplicates(subset=['cast_id'], keep='first', inplace=True)

    insert_query = "INSERT INTO credits_cast (cast_id, `character`, credit_id, gender, id, `name`, `order`, profile_path,movie_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)"
    for index, row in credits_cast.iterrows():
        cursor.execute(insert_query, (row['cast_id'], row['character'],row['credit_id'], row['gender'],row['id'], row['name'],row['order'],row['profile_path'],row['movie_id']))
    print("Inserted Data")

    # Commit changes and close cursor
    connection.commit()
    cursor.close()

if connection.is_connected():
    connection.close()
