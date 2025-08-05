import argparse

import pandas as pd
import constants
import mysql.connector
from mysql.connector import Error
import numpy as np

print_executed = False
def get_db_credentials():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='Process dataset and create database')
    
    # Add command-line arguments
    parser.add_argument('host', type=str, help='host address of databse')
    parser.add_argument('user', type=str, help='database user')
    parser.add_argument('password', type=str, help='database password')

    try:
        # Parse the command-line arguments
        args = parser.parse_args()
    except argparse.ArgumentError:
        print('Error: Required arguments not provided')
        quit()
    
    return { 'host': args.host, 'user': args.user, 'password': args.password }

def get_db_connection(host, user, password, database=None):
    global print_executed
    try:    
        if (database == None):
            connection = mysql.connector.connect(host=host, user=user, password=password)
        else:
            connection = mysql.connector.connect(host=host, user=user, password=password, database=database)       
        if not print_executed:
            print(f"Sucessfully connected to AWS RDS as {user} user.")
            print("AWS RDS Connection Details:")
            print(f"Host: {connection.server_host}")
            print(f"Port: {connection.server_port}")
            print(f"User: {connection.user}")
            print(f"Database: {connection.database}")  
            print_executed = True
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION();")
            db_version = cursor.fetchone()
            print("MySQL Server version:", db_version)
    except Error as e:
        print(f"Error while connecting to AWS RDS as {user} user.", e)
        quit()
    
    return connection

def execute_query_with_params(host, user, password, database, query, param_values):
    try:

        cnx = get_db_connection(host,user,password,database)
        cursor = cnx.cursor()
        cursor.execute(query, param_values)
        rows = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]
        df = pd.DataFrame(rows, columns=column_names)
        cursor.close()
        cnx.close()
        return df

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def exexute_and_print_query_results(host,user,password, query, param_values, header):
    result_df = execute_query_with_params(host,user,password,constants.DATABASE_NAME, query, param_values)
    
    if result_df is not None:
        print(header)
        print(result_df)
    else:
        print("Query execution failed.")
    
def fetch_top_movie_by_revenue(host,user,password):
    
    query = """SELECT 
                    original_title AS 'Movie Title',
                    FORMAT(budget / 1000000, 2) AS 'Budget in Millions',
                    FORMAT(revenue / 1000000, 2) AS 'Revenue in Millions',
                    FORMAT((revenue - budget) / 1000000, 2) AS 'Profit in Millions'
                FROM
                    movie_metadata
                ORDER BY revenue DESC
                LIMIT 10;
    """
    
    param_values = ()
    header = "Top 10 Movies based on revenue generated"
    exexute_and_print_query_results(host,user,password, query, param_values, header)
    

def num_movies_genre(host,user,password):
    query="""
    SELECT 
        genres.name AS 'Genres', COUNT(*) AS 'Movies Count'
    FROM
        movie_genres
            JOIN
        genres ON genres.genres_id = movie_genres.genres_id
    GROUP BY movie_genres.genres_id;
    """
    
    param_values = ()
    header = "Number of Movies in Each Genre"
    exexute_and_print_query_results(host,user,password, query, param_values, header)

def top_popular_movies_in_genres(host,user,password):
    query="""
    WITH RankedMovies AS (
    SELECT
        genres.name,
        movie_metadata.title,
        ROW_NUMBER() OVER(PARTITION BY movie_genres.genres_id ORDER BY movie_metadata.popularity DESC) AS genre_rank
    FROM
        movie_genres 
    JOIN
        movie_metadata  ON movie_metadata.tmdb_id = movie_genres.tmdb_id
	JOIN 
       genres on genres.genres_id = movie_genres.genres_id
    )
    SELECT
	    genre_rank AS 'Popularity Rank',
        name AS 'Genres',
        title AS 'Movie name'
    FROM
        RankedMovies
    WHERE
        genre_rank <= 5;
    """
    param_values = ()
    header = "Top 5 Popular Movies in Each Genre"
    exexute_and_print_query_results(host,user,password, query, param_values, header)
    
def top_keywords(host,user,password):
    query="""
    SELECT 
        keywords.name AS 'Top 15 Keywords'
    FROM
        movie_keywords
            JOIN
        keywords ON keywords.keywords_id = movie_keywords.keywords_id
    GROUP BY movie_keywords.keywords_id
    ORDER BY COUNT(*) DESC
    LIMIT 15;
    """
    param_values = ()
    header = "Top 15 Keywords Used in Movies"
    exexute_and_print_query_results(host,user,password, query, param_values, header)

def weighted_rating(host,user,password):
    query="""
    SELECT 
        original_title AS 'Movie',
        vote_average,
        vote_count,
        ((vote_average * vote_count) + ((SELECT 
            AVG(vote_average)
        FROM
            movie_metadata) * 109)) / (vote_count + 109) AS weighted_rating
    FROM
        movie_metadata
    ORDER BY weighted_rating DESC
    LIMIT 5;
    """
    param_values = ()
    header = "Top 5 Movies based on Weighted Votes"
    exexute_and_print_query_results(host,user,password, query, param_values, header)

def list_stored_procedures(host,user,password):
    query="SELECT routine_name FROM information_schema.routines WHERE routine_type = 'PROCEDURE' AND routine_schema = %s"
        # Execute the query
    param_values = ((constants.DATABASE_NAME,))
    header = "List of Stored Procedures"
    exexute_and_print_query_results(host,user,password, query, param_values, header)
    
def list_triggers(host,user,password):
    query="SELECT trigger_name, event_object_table FROM information_schema.triggers WHERE trigger_schema = %s"
        # Execute the query
    param_values = ((constants.DATABASE_NAME,))
    header = "List of Triggers"
    exexute_and_print_query_results(host,user,password, query, param_values, header)
    
def main():
    
    db_credentilas = get_db_credentials()
    host=db_credentilas['host']
    user=db_credentilas['user']
    password=db_credentilas['password']
    
    get_db_connection(host,user,password, constants.DATABASE_NAME)
    
    fetch_top_movie_by_revenue(host,user,password)
    num_movies_genre(host,user,password)
    top_popular_movies_in_genres(host,user,password)
    top_keywords(host,user,password)
    weighted_rating(host,user,password)
    list_stored_procedures(host,user,password)
    list_triggers(host,user,password) 
    
if __name__=="__main__": 
	main()