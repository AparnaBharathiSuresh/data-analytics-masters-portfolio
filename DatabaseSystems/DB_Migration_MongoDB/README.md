# data225-lab2

## Source code for preprocessing data from csv files and loading into TDMB databse on MongoDB cluster

Instructions to execute the code:
- clone the repo and create developer branch (git checkout -b "branch-name")
- Copy the dataset *.csv file to 'DATA225-LAB1/Data_Processing/res/' folder
- Create and configure MongoDB cluster on MongoDB Atlas and get username and password for accessing the database
- Run the main program:
```
    python Data_Processing/src/main.py username password
```


NOTE: If running on windows: In data_processing.py get_dataset() function uncomment:
file = f'{constants.DATA_SET_PATH}\\{file_name}.{constants.DATA_SET_EXTENSION}'

