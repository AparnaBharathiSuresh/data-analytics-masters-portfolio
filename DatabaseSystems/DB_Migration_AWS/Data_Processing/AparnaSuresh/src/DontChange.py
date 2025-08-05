import pandas as pd
import ast
#import seaborn as sns

df = pd.read_csv("C:/Users/aparn/OneDrive/Documents/SJSU/DATA_225/Lab/Lab_1/DATA225-Lab1-main/DATA225-Lab1/res/keywords.csv")

df['keywords'] = df['keywords'].apply(ast.literal_eval)
index = 0

for dictionary in df['keywords']:
    for dict_entry in dictionary:
        for key,value in dict_entry.items():
            print(df['id'][index],key,value)
    index+=1