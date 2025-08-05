import ast
import json
import argparse
import constants
import numpy as np
import pandas as pd

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

def convert_to_ejson(df, index, row, column_name):
    try:
        json_object = ast.literal_eval(row[column_name])
        ejson_string = json.dumps(json_object, separators=(',', ':'), default=str)
        df.at[index, column_name] = json.loads(ejson_string)
        
    except Exception as e:
        #print(e)
        df.at[index, column_name] = None