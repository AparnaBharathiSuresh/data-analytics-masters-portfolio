import pandas as pd
import ast
import mysql.connector

df = pd.read_csv("C:/Users/aparn/OneDrive/Documents/SJSU/DATA_225/Lab/Lab_1/DATA225-Lab1-main/DATA225-Lab1/res/credits.csv")
credits_crew = pd.DataFrame(columns=['credit_id','department','gender','crew_id','job','name','profile_path','movie_id'])

df['crew'] = df['crew'].apply(ast.literal_eval)


creditid_list = []
department_list = []
gender_list=[]
id_list=[]
job_list=[]
name_list=[]
profilepath_list=[]

for dictionary in df['crew']:
    for dict_entry in dictionary:
        if 'credit_id' in dict_entry:
            creditid_list.append(dict_entry['credit_id'])
        if 'department' in dict_entry:
            department_list.append(dict_entry['department'])
        if 'gender' in dict_entry:
            gender_list.append(dict_entry['gender'])
        if 'id' in dict_entry:
            id_list.append(dict_entry['id'])
        if 'job' in dict_entry:
            job_list.append(dict_entry['job'])
        if 'name' in dict_entry:
            name_list.append(dict_entry['name'])
        if 'profile_path' in dict_entry:
            profilepath_list.append(dict_entry['profile_path'])

credits_crew['credit_id'] = creditid_list
credits_crew['department'] = department_list
credits_crew['gender'] = gender_list
credits_crew['crew_id'] = id_list
credits_crew['job'] = job_list
credits_crew['name'] = name_list
credits_crew['profile_path'] = profilepath_list
credits_crew['movie_id']=df['id']

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
    drop_table_query = "DROP TABLE IF EXISTS credits_crew"
    cursor.execute(drop_table_query)
    print("Dropped table")

    cursor.execute("CREATE TABLE credits_crew(credit_id VARCHAR(200),department VARCHAR(200),gender INT,crew_id INT PRIMARY KEY,job VARCHAR(200),`name` VARCHAR(200),profile_path VARCHAR(200),movie_id INT)")
    print("Created table")

    credits_crew.drop_duplicates(subset=['crew_id'], keep='first', inplace=True)

    insert_query = "INSERT INTO credits_crew (credit_id,department,gender,crew_id,job,name,profile_path,movie_id) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
    for index, row in credits_crew.iterrows():
        cursor.execute(insert_query, (row['credit_id'], row['department'],row['gender'], row['crew_id'],row['job'], row['name'],row['profile_path'],row['movie_id']))
    print("Inserted Data")

    # Commit changes and close cursor
    connection.commit()
    cursor.close()

if connection.is_connected():
    connection.close()
