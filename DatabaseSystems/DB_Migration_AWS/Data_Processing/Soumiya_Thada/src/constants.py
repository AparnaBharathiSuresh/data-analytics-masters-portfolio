DATA_SET_PATH = 'Data_Processing/Soumiya_Thada/res'
DATA_SET_EXTENSION = 'csv'
MOVIES_METADATA = 'Movies_Metadata'
KEYWORDS = 'keywords'
CREDITS = 'credits'
LINKS = 'links'
RATINGS = 'ratings_small'

# Movies_Metadata csv file headers
HEADER_ID = 'id'
HEADER_TITLE = 'title'
HEADER_GENRES = 'genres',['genres_id','name'], ['varchar(255) PRIMARY KEY', 'VARCHAR(255)'], ['id','name'], 'id','id'
HEADER_PRODUCTION_COMPANIES = 'production_companies', ['production_companies_id','name'], ['varchar(255) PRIMARY KEY', 'VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'], ['id','name'], 'id','id'
HEADER_BELONGS_TO_COLLECTION = 'belongs_to_collection', ['belongs_to_collection_id', 'name', 'poster_path', 'backdrop_path'], ['varchar(255) PRIMARY KEY', 'VARCHAR(255)', 'VARCHAR(255)', 'VARCHAR(255)'], ['id', 'name', 'poster_path', 'backdrop_path'], 'id','id'
HEADER_PRODUCTION_COUNTRIES = 'production_countries', ['production_countries_id', 'name'], ['varchar(255) PRIMARY KEY','VARCHAR(255)'], ['iso_3166_1','name'], 'id','iso_3166_1'
HEADER_SPOKEN_LANGUAGES = 'spoken_languages', ['spoken_languages_id', 'name'], ['varchar(255) PRIMARY KEY', 'VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'], ['iso_639_1','name'], 'id','iso_639_1'

HEADER_KEYWORDS = 'keywords',['keywords_id','name'], ['varchar(255) PRIMARY KEY', 'VARCHAR(255)'], ['id','name'], 'id','id'

HEADER_CAST = 'credit', ['credit_id', 'cast_id', 'id', 'character_name', 'gender','name','order_num','profile_path'], ['VARCHAR(255) PRIMARY KEY', 'int', 'int', 'VARCHAR(500)', 'int','VARCHAR(255)','int','VARCHAR(255)'], ['credit_id','cast_id','id','character','gender','name','order','profile_path'], 'id','credit_id'
HEADER_CREW = 'credit', ['credit_id', 'id', 'department', 'gender','name','job','profile_path'], ['VARCHAR(255) PRIMARY KEY', 'int', 'VARCHAR(255)', 'int','VARCHAR(255)','VARCHAR(255)','VARCHAR(255)'], ['credit_id', 'id', 'department', 'gender','name','job','profile_path'], 'id','credit_id'


movies_meta_data_headers = [HEADER_ID]
primary_table_headers = [HEADER_BELONGS_TO_COLLECTION, HEADER_GENRES, HEADER_PRODUCTION_COMPANIES, HEADER_PRODUCTION_COUNTRIES, HEADER_SPOKEN_LANGUAGES]
keywords_table_headers = [HEADER_KEYWORDS]

#[HEADER_BELONGS_TO_COLLECTION, HEADER_GENRES, HEADE_PRODUCTION_COMPANIES, HEADER_PRODUCTION_COUNTRIES, HEADER_SPOKEN_LANGUAGES]



DATABASE_NAME = 'tmdb'
MOVIES_METADATA_TABLE = 'movie_metadata'
LINKS_TABLE = 'links'
RATINGS_TABLE = 'ratings'
HEADER_TMDB_ID = 'tmdb_id'


