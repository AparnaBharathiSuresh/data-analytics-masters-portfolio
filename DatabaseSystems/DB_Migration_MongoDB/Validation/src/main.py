import validate 

def main():
    db_credentilas = validate.get_db_credentials() 
    user=db_credentilas['user']
    password=db_credentilas['password']

    validate.test_mongodb_connection(user, password)
    validate.test_migration_valdiation(user, password)
    
# call main function
if __name__=="__main__": 
	main()