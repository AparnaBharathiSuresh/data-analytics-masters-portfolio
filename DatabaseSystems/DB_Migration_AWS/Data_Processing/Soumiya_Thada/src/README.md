# DATA225-Lab1

## Source code for preprocessing data from csv files and loading into MySQL TDMB databse

Instructions to execute the code:
- clone the repo and create developer branch (git checkout -b "branch-name")
- Copy the dataset *.csv file to DATA225-LAB1/Data_Processing/Soumiya_Thada/res/ folder
- Launch MySQL
- Run the main program:
```
    python Data_Processing/Soumiya_Thada/src/main.py host username password
```
    - use localhost for running on local machine
    - username and password for MySQL workbench

NOTE: If running on windows:
In data_processing.py get_dataset() function uncomment:
```
file = f'{constants.DATA_SET_PATH}\\{file_name}.{constants.DATA_SET_EXTENSION}'
```
