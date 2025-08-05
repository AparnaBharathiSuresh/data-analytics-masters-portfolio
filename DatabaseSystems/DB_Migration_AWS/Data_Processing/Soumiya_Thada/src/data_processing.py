import pandas as pd
import constants
import db_manager
import ast
import numpy as np
    

def get_dataset(file_name, nrows=None, low_memory=False):
    file = f'{constants.DATA_SET_PATH}/{file_name}.{constants.DATA_SET_EXTENSION}'
    # For windows use \\ as filepath delimeter
    #file = f'{constants.DATA_SET_PATH}\\{file_name}.{constants.DATA_SET_EXTENSION}'
    df = pd.read_csv(filepath_or_buffer=file, nrows=nrows, low_memory=low_memory)
    return df

def remove_duplicates(df, headers=None):
    df_processed = None
    if headers == None:
        df_processed = df.drop_duplicates()
        return df_processed
    
    for header in headers:
        df_processed = df.drop_duplicates(subset=[header])
    return df_processed

def map_adult_value(value):
    if value == 'TRUE' or value == True:
        return 1
    elif value == 'FALSE' or value == False:
        return 0
    else:
        return np.nan 
    
def remove_nullrows(df, headers=None):
    df_processed = None
    if headers == None:
        df_processed = df.dropna()
        return df_processed
    
    for header in headers:
        df_processed = df.dropna(subset=[header])
    return df_processed

def replace_non_integer(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return np.nan

def clean_df(df, headers=None):
    df_processed = None
    df_processed = remove_duplicates(df, headers)
    df_processed = remove_nullrows(df_processed, headers)
    return df_processed


def load_movies_metadata(host, user,password):
    df_movie_metadata = get_dataset(file_name=constants.MOVIES_METADATA)#, nrows=30)
    df_movie_metadata['adult'] = df_movie_metadata['adult'].map(map_adult_value)
    df_movie_metadata = df_movie_metadata.dropna(subset=['adult'])
    df_movie_metadata['adult'] = df_movie_metadata['adult'].astype(int)
    df_movie_metadata['id'] = df_movie_metadata['id'].apply(replace_non_integer)
    df_movie_metadata = clean_df(df_movie_metadata, headers=constants.movies_meta_data_headers)
    df_movie_metadata['id'] = df_movie_metadata['id'].astype(int)
    df_movie_metadata = df_movie_metadata.replace(np.nan, None)
    
    prepare_movie_metadata_parent_table(df_movie_metadata, host, user, password, constants.DATABASE_NAME)
    for header in constants.primary_table_headers:
        prepare_parent_and_connecting_tables(df_movie_metadata, header, host, user, password, constants.DATABASE_NAME)
 
def load_keywords(host, user,password):
    df_keywords = get_dataset(file_name=constants.KEYWORDS) #, nrows=30)
    df_keywords = clean_df(df_keywords, ['id'])
    
    for header in constants.keywords_table_headers:
        prepare_parent_and_connecting_tables(df_keywords, header, host, user, password, constants.DATABASE_NAME) 
    
    
def load_links(host, user,password):   
    df_links = get_dataset(file_name=constants.LINKS)#, nrows=30)
    df_links = clean_df(df_links, ['movieId','tmdbId'])
    df_links = df_links.replace(np.nan, None)
    prepare_links_table(df_links, host, user, password, constants.DATABASE_NAME) 
    
def load_ratings(host, user,password):  
    df_ratings = get_dataset(file_name=constants.RATINGS)#, nrows=30)
    df_ratings = df_ratings.replace(np.nan, None)  
    
    prepare_ratings_table(df_ratings, host, user, password, constants.DATABASE_NAME) 
    
def load_credits(host, user,password):
    df_credits = get_dataset(file_name=constants.CREDITS)#, nrows=1)
    df_credits = clean_df(df_credits, ['id'])
    df_credits = df_credits.replace(np.nan, None) 
    
    df_credits = df_credits.rename(columns={'cast': 'credit'})
    prepare_parent_and_connecting_tables(df_credits, constants.HEADER_CAST, host, user, password, constants.DATABASE_NAME)
    db_manager.rename_table(host, user, password,constants.DATABASE_NAME,'credit','casts')
    db_manager.rename_table(host, user, password,constants.DATABASE_NAME,'movie_credit','movie_casts') 
    df_credits = df_credits.rename(columns={'credit': 'cast'})
    df_credits = df_credits.rename(columns={'crew': 'credit'})
    prepare_parent_and_connecting_tables(df_credits, constants.HEADER_CREW, host, user, password, constants.DATABASE_NAME)
    db_manager.rename_table(host, user, password,constants.DATABASE_NAME,'credit','crews')
    db_manager.rename_table(host, user, password,constants.DATABASE_NAME,'movie_credit','movie_crews') 
    
    
def prepare_parent_and_connecting_data(df, column_name, corr_column1, corr_column2):
    column1 = constants.HEADER_TMDB_ID
    column2 = f'{column_name}_id'
    #corr_column1 = constants.HEADER_ID
    #corr_column2 = constants.HEADER_ID
     
    # Initialize a dictionary to store unique values for each key
    connecting_table_data = {}
    connecting_table_data[column1] = []
    connecting_table_data[column2] = []
    
    parent_table_data = {}
    
    # Iterate over each row in the DataFrame
    for _, row in df.iterrows():
        json_array = []
        try:
            # Load JSON data from the specified column
            json_object = ast.literal_eval(row[column_name])
            if type(json_object) == dict:
                json_array = [json_object]
            elif type(json_object) == list:
                json_array = json_object
            else:
                print(f'Unsupported json object found: {type(json_object)} in column {column_name}')
        except SyntaxError as e:
            # Handle syntax errors
            # print(f"Ubale to extract json data from {column_name}")
            # print("SyntaxError:", e)
            pass
        except ValueError as e:
            # Handle value errors
            # print(f"Ubale to extract json data from {column_name}")
            # print("ValueError:", e)
            pass
        except Exception as e:
            # Handle other types of exceptions
            # print(f"Ubale to extract json data from {column_name}")
            # print("An error occurred:", e)
            pass
       
        primary_key = 1
        # Iterate over each JSON object in the array
        for json_entry in json_array:
            """ values = [str(value) for value in json_entry.values()]
            concatenated_string = ''.join(values)
            primary_key = hash(concatenated_string) """
            
            try:
                connecting_table_data[column1].append(row[corr_column1])
                # Check if the specified key exists in the JSON object
                #if corr_column2 in json_entry:
                    # If the key exists, append its value to the list
                connecting_table_data[column2].append(json_entry[corr_column2])
               # else:
                    # If the key does not exists, append a default primary key to the list
                    # Concatenate values into a single string
                    #connecting_table_data[column2].append(primary_key)
                    
            except Exception as e:
                print("Error adding entries in connecting_table_data", e)
             
            """ if constants.HEADER_ID not in json_entry.keys():
                if constants.HEADER_ID in parent_table_data:
                    parent_table_data[constants.HEADER_ID].append(primary_key)
                # If the key does not exist in the dictionary, create a new list for the key and append the value
                else:    
                    parent_table_data[constants.HEADER_ID] = [primary_key] """

            #parent_table_data[constants.HEADER_ID] = primary_key
            for key, value in json_entry.items():
                # If the key already exists in the dictionary and the value is not already present in the list,
                # append the value to its corresponding list
                if key in parent_table_data:
                    parent_table_data[key].append(value)
                # If the key does not exist in the dictionary, create a new list for the key and append the value
                else:    
                    parent_table_data[key] = [value]
                    
        
    """ if constants.HEADER_ID not in parent_table_data:
        # If primary key does not exist in parent_table_data add the primary key and its values
        length_of_parent_table = len(parent_table_data[next(iter(parent_table_data))])
        parent_table_data[constants.HEADER_ID] = [primary_key_value for primary_key_value in range(1, length_of_parent_table+1)] """

    #print(f'parent_table_data: \n {parent_table_data}')
    #print(f'\nconnecting_table_data: \n {connecting_table_data}')
    return parent_table_data, connecting_table_data
    
def prepare_movie_metadata_parent_table(df, host, user, password, database):
    table_name = constants.MOVIES_METADATA_TABLE
    headers = ['id','title','adult','budget', 'homepage', 'imdb_id', 'original_language', 'original_title', 'overview', 'popularity', 'poster_path', 'release_date', 'revenue', 'runtime', 'status', 'tagline', 'video', 'vote_average', 'vote_count']
    
    create_table_query = f"""
        CREATE TABLE movie_metadata (
        {constants.HEADER_TMDB_ID} int PRIMARY KEY,
        title VARCHAR(255),
        adult boolean,
        budget bigint,
        homepage varchar(255),
        imdb_id int UNIQUE,
        original_language varchar(255),
        original_title varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        overview varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        popularity float,
        poster_path varchar(255),
        release_date varchar(255),
        revenue bigint,
        runtime int,
        status varchar(255),
        tagline varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        video boolean,
        vote_average float,
        vote_count int   
    )
    """
    
    insert_table_query = f"""
            INSERT INTO Movie_Metadata 
            ({constants.HEADER_TMDB_ID}, title, adult, budget, homepage, imdb_id, original_language, original_title, overview, popularity, poster_path, release_date, revenue, runtime, status, tagline, video, vote_average, vote_count) 
            VALUES (%s, %s, %s, %s, %s, SUBSTRING(%s, 3), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

    db_manager.create_insert_table(df, host, user, password, database, table_name, create_table_query, headers, insert_table_query)

def prepare_links_table(df, host, user, password, database):
    table_name = constants.LINKS_TABLE
    headers = ['movieId','imdbId','tmdbId']
    
    create_table_query = f"""
        CREATE TABLE {table_name} (
        movie_id int PRIMARY KEY,
        imdb_id int,
        tmdb_id int,
        FOREIGN KEY (tmdb_id) REFERENCES movie_metadata(tmdb_id)
    )
    """
    
    insert_table_query = f"""
            INSERT INTO {table_name} 
            (movie_id, imdb_id, tmdb_id) 
            VALUES (%s, %s, %s)
        """

    db_manager.create_insert_table(df, host, user, password, database, table_name, create_table_query, headers, insert_table_query)

def prepare_ratings_table(df, host, user, password, database):
    table_name = constants.RATINGS_TABLE
    headers = ['userId','movieId','rating','timestamp']
    
    create_table_query = f"""
        CREATE TABLE {table_name} (
        user_id int,
        movie_id int,
        rating float,
        timestamp TIMESTAMP,
        PRIMARY KEY(user_id,movie_id),
        FOREIGN KEY (movie_id) REFERENCES links(movie_id)
    )
    """
    
    insert_table_query = f"""
            INSERT INTO {table_name} 
            (user_id, movie_id, rating, timestamp) 
            VALUES (%s, %s, %s, FROM_UNIXTIME(%s))
        """

    db_manager.create_insert_table(df, host, user, password, database, table_name, create_table_query, headers, insert_table_query)
       
              
def prepare_parent_and_connecting_tables(df, header, host, user, password, database):
    column_name = header[0]
    table_column_names_list = header[1]
    data_types_list = header[2] 
    header_list = header[3]
    corr_column1 = header[4]
    corr_column2 = header[5]

    parent_table_data, connecting_table_data = prepare_parent_and_connecting_data(df, column_name, corr_column1, corr_column2)
    
    
    parent_table_data = pd.DataFrame(parent_table_data)
    
    parent_table_data = clean_df(parent_table_data, [corr_column2])
    connecting_table_data = pd.DataFrame(connecting_table_data)
    
    parent_table_name = column_name
    
    create_table_query = get_create_table_query(parent_table_name, table_column_names_list, data_types_list)
    insert_table_query = get_insert_query(parent_table_name, table_column_names_list)
    

    db_manager.create_insert_table(parent_table_data, host, user, password, database, parent_table_name, create_table_query, header_list, insert_table_query)
    
    connecting_table_name = f'movie_{column_name}'
    header_list = [constants.HEADER_TMDB_ID,f'{column_name}_id']
         
    create_table_query = f"""
        CREATE TABLE {connecting_table_name} (
        {constants.HEADER_TMDB_ID} int,
        {column_name}_id varchar(255),
        Foreign key({constants.HEADER_TMDB_ID}) references {constants.MOVIES_METADATA_TABLE}({constants.HEADER_TMDB_ID}),
        Foreign key({column_name}_id) references {parent_table_name}({column_name}_id),
        Primary Key({constants.HEADER_TMDB_ID}, {column_name}_id)
    )
    """
    
    insert_table_query = f"""
        INSERT INTO {connecting_table_name} 
        ({constants.HEADER_TMDB_ID}, {column_name}_id)
        VALUES (%s, %s)
    """
    
    db_manager.create_insert_table(connecting_table_data, host, user, password, database, connecting_table_name, create_table_query, header_list, insert_table_query)
    
    
    
def get_create_table_query(table_name, column_names, data_types):
    create_table_query = f"CREATE TABLE {table_name} ("
    for column_name, data_type in zip(column_names, data_types):

        create_table_query += f"\n\t{column_name} {data_type},"
    create_table_query = create_table_query.rstrip(',') + "\n);"

    #print("SQL Table Creation Query:")
    #print(create_table_query)
    
    return create_table_query
    
def get_insert_query(table_name, column_names):
    insert_query = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ("
    insert_query += ', '.join(['%s' for _ in range(len(column_names))])
    insert_query += ");"

    #print("INSERT Query:")
    #print(insert_query)
    
    return insert_query
        
        