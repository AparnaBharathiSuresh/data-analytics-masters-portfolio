import constants
import numpy as np
import data_processing
from pymongo import MongoClient
import pandas as pd
import ast

def main():
    db_credentilas = data_processing.get_db_credentials() 
    user=db_credentilas['user']
    password=db_credentilas['password']
    

    # Read CSV file into DataFrame
    df_movieMetadata = data_processing.get_dataset('movies_metadata')#, nrows = n_rows)
    
    
   
    
    df_keywords = data_processing.get_dataset('keywords')#, nrows = n_rows)
    df_links = data_processing.get_dataset('links')#, nrows = n_rows)
    df_ratings = data_processing.get_dataset('ratings_small')#, nrows = n_rows)
    
    credits_df = data_processing.get_dataset('credits')#, nrows = n_rows)
    
    #clean data for keywords file
    df_keywords['id'] = df_keywords['id'].apply(data_processing.replace_non_integer)
    df_keywords= data_processing.clean_df(df_keywords, headers=['id'])
    df_keywords['id'] = df_keywords['id'].astype(int)
    df_keywords = df_keywords.replace(np.nan,None)
    
    #clean data for links file
    df_links = df_links.rename(columns={'tmdbId': 'id'})#rename column from tmdbId to id
    df_links = df_links.replace(np.nan,None)
    # Replace non-finite values with -1 
    df_links.fillna(-1, inplace=True)
    df_links['movieId'] = df_links['movieId'].apply(data_processing.replace_non_integer)
    df_links['imdbId'] = df_links['imdbId'].apply(data_processing.replace_non_integer)
    df_links['id'] = df_links['id'].apply(data_processing.replace_non_integer)
    df_links['movieId'] = df_links['movieId'].astype(int)
    df_links['imdbId'] = df_links['imdbId'].astype(int)
    df_links['id'] = df_links['id'].astype(int)
    
    #clean data for ratings file
    df_ratings['userId'] = df_ratings['userId'].apply(data_processing.replace_non_integer)
    df_ratings['movieId'] = df_ratings['movieId'].apply(data_processing.replace_non_integer)
    df_ratings['rating'] = df_ratings['rating'].apply(data_processing.replace_non_integer)
    df_ratings['timestamp'] = pd.to_datetime(df_ratings['timestamp'], unit='s')
    df_ratings['userId'] = df_ratings['userId'].astype(int)
    df_ratings['movieId'] = df_ratings['movieId'].astype(int)
    df_ratings['rating'] = df_ratings['rating'].astype(float)
    df_ratings = df_ratings.replace(np.nan,None)
    # Convert NaT values to None
    
    #df_ratings['timestamp'] = df_ratings['timestamp'].fillna(df_ratings['timestamp'].shift().add(pd.Timedelta('1min')))
    df_ratings['timestamp'] = df_ratings['timestamp'].apply(lambda x: x.strftime('%Y-%m-%d')if not pd.isnull(x) else '')
    
    #MERGE Movie_metadata and Keywords
    df_movie_key = pd.merge(df_movieMetadata, df_keywords, on='id', how='left')
    
    #MERGE Movie_metadata and links
    df_movie_link_key = pd.merge(df_movie_key, df_links, on='id', how='left')
    
    # Group by movieId and create a list of dictionaries for each group
    grouped_ratings = df_ratings.groupby('movieId').apply(lambda x: x[['userId', 'rating', 'timestamp']].to_dict('records')).reset_index(name='ratings')

    #MERGE Movie_metadata and ratings
    df = pd.merge(df_movie_link_key, grouped_ratings, on='movieId', how='left')
    
    for field in ['cast', 'crew']:
        credits_df[field] = credits_df[field].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else None)
    df = pd.merge(df, credits_df, on='id', how='left')

    df['adult'] = df['adult'].map(data_processing.map_adult_value)
    df = df.dropna(subset=['adult'])
    df['adult'] = df['adult'].astype(int)
    df['id'] = df['id'].apply(data_processing.replace_non_integer)
    df = data_processing.clean_df(df, headers=['id'])
    df['id'] = df['id'].astype(int)
    df = df.replace(np.nan, None)
    
    for index, row in df.iterrows():
        
        data_processing.convert_to_ejson(df, index, row, 'belongs_to_collection')
        data_processing.convert_to_ejson(df, index, row, 'genres')
        data_processing.convert_to_ejson(df, index, row, 'production_companies')
        data_processing.convert_to_ejson(df, index, row, 'production_countries')
        data_processing.convert_to_ejson(df, index, row, 'spoken_languages')
        data_processing.convert_to_ejson(df, index, row, 'keywords')


    # Connect to MongoDB
    conn_string = f'mongodb+srv://{user}:{password}@cluster0.8cy6qn7.mongodb.net/'
    client = MongoClient(conn_string)
    db = client[constants.DATABASE_NAME]  
    collection = db[constants.COLLECTION_NAME]  
        
    # Convert DataFrame to dictionary
    data = df.to_dict(orient='records')
    #print(data)

    # Insert data into MongoDB
    collection.insert_many(data)
    
    print("Data Inserted successfully")


    # Update data
    """ for document in data:
        filter = {"id": document["id"]}
        update = {"$set": document}
        collection.update_many(filter, update, upsert=True) """
      
    
# call main function
if __name__=="__main__": 
	main()