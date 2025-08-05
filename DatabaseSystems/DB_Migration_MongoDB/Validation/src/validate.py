import argparse
import constants
from pymongo import MongoClient

def get_db_credentials():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='Process dataset and create database')

    parser.add_argument('user', type=str, help='database user')
    parser.add_argument('password', type=str, help='database password')

    try:
        # Parse the command-line arguments
        args = parser.parse_args()
    except argparse.ArgumentError:
        print('Error: Required arguments not provided')
        quit()
    
    return { 'user': args.user, 'password': args.password }

def test_migration_valdiation(user, password):
    try:
        conn_string = f'mongodb+srv://{user}:{password}@cluster0.8cy6qn7.mongodb.net/'

        client = MongoClient(conn_string)
        db_names = client.list_database_names()
        print("Connection successful")
        print("MongoDB server address:", client.address)
        
        print("Available databases:", db_names)
        
        db = client[constants.DATABASE_NAME]  
        collection = db[constants.COLLECTION_NAME]
        document_count = collection.count_documents({})
        print(f"Document count in tmdb.movie_metadata collection:", document_count)
    
        documents = collection.find().limit(5)
        first_document = documents[0]
        print("Fields present in the collection:")
        for key in first_document.keys():
            print(key)
        
    except Exception as e:
        print("Connection failed:", e)

def test_mongodb_connection(user, password):
    try:
        conn_string = f'mongodb+srv://{user}:{password}@cluster0.8cy6qn7.mongodb.net/'
        
        client = MongoClient(conn_string)
        server_info = client.server_info()
        
        print("Connection successful")
        print("MongoDB server address:", client.address)
        
    except Exception as e:
        print("Connection failed:", e)