CREATE VIEW movie_details_view AS
SELECT mm.*, mbc.belongs_to_collection_id, mg.genres_id, mk.keywords_id
FROM movie_metadata AS mm
JOIN movie_belongs_to_collection AS mbc ON mm.tmdb_id = mbc.tmdb_id
JOIN movie_genres AS mg ON mm.tmdb_id = mg.tmdb_id
JOIN movie_keywords AS mk ON mm.tmdb_id = mk.tmdb_id;

SELECT * FROM movie_details_view;


CREATE TABLE movies_production_companies_countries AS SELECT M.TMDB_ID AS Movie_ID,M.TITLE AS Movie_title,MPC.production_companies_id AS Prod_company_id,PC.`name` AS Prod_company_name,C.production_countries_id AS Prod_country_id,C.`name` AS Prod_Country_name 
FROM `movie_metadata` M 
JOIN `movie_production_companies` MPC ON M.TMDB_ID=MPC.TMDB_ID
JOIN `production_companies` PC ON MPC.production_companies_id=PC.production_companies_id
JOIN `movie_production_countries` MC ON M.TMDB_ID=MC.TMDB_ID
JOIN `production_countries` C ON MC.production_countries_id=C.production_countries_id order by  M.TMDB_ID ;

select * from movies_production_companies_countries;

DROP TABLE movies_production_companies_countries;


CREATE TABLE movie_test(
movie_id INT,
movie_title VARCHAR(200),
movie_rating FLOAT
);


INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (1,"Avatar",5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (2,"Avatar",2.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (3,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (4,"Avatar",3.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (5,"Avatar",2);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (6,"Avatar",3);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (7,"Avatar",4.5);

INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (1,"Avatar",5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (2,"Avatar",2.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (3,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (4,"Avatar",3.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (5,"Avatar",2);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (6,"Avatar",3);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (7,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (1,"Avatar",5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (2,"Avatar",2.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (3,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (4,"Avatar",3.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (5,"Avatar",2);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (6,"Avatar",3);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (7,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (1,"Avatar",5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (2,"Avatar",2.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (3,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (4,"Avatar",3.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (5,"Avatar",2);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (6,"Avatar",3);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (7,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (1,"Avatar",5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (2,"Avatar",2.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (3,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (4,"Avatar",3.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (5,"Avatar",2);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (6,"Avatar",3);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (7,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (1,"Avatar",5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (2,"Avatar",2.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (3,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (4,"Avatar",3.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (5,"Avatar",2);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (6,"Avatar",3);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (7,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (1,"Avatar",5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (2,"Avatar",2.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (3,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (4,"Avatar",3.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (5,"Avatar",2);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (6,"Avatar",3);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (7,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (1,"Avatar",5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (2,"Avatar",2.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (3,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (4,"Avatar",3.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (5,"Avatar",2);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (6,"Avatar",3);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (7,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (1,"Avatar",5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (2,"Avatar",2.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (3,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (4,"Avatar",3.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (5,"Avatar",2);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (6,"Avatar",3);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (7,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (1,"Avatar",5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (2,"Avatar",2.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (3,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (4,"Avatar",3.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (5,"Avatar",2);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (6,"Avatar",3);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (7,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (1,"Avatar",5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (2,"Avatar",2.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (3,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (4,"Avatar",3.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (5,"Avatar",2);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (6,"Avatar",3);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (7,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (1,"Avatar",5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (2,"Avatar",2.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (3,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (4,"Avatar",3.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (5,"Avatar",2);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (6,"Avatar",3);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (7,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (1,"Avatar",5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (2,"Avatar",2.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (3,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (4,"Avatar",3.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (5,"Avatar",2);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (6,"Avatar",3);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (7,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (1,"Avatar",5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (2,"Avatar",2.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (3,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (4,"Avatar",3.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (5,"Avatar",2);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (6,"Avatar",3);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (7,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (1,"Avatar",5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (2,"Avatar",2.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (3,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (4,"Avatar",3.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (5,"Avatar",2);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (6,"Avatar",3);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (7,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (1,"Avatar",5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (2,"Avatar",2.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (3,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (4,"Avatar",3.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (5,"Avatar",2);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (6,"Avatar",3);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (7,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (1,"Avatar",5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (2,"Avatar",2.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (3,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (4,"Avatar",3.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (5,"Avatar",2);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (6,"Avatar",3);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (7,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (1,"Avatar",5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (2,"Avatar",2.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (3,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (4,"Avatar",3.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (5,"Avatar",2);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (6,"Avatar",3);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (7,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (1,"Avatar",5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (2,"Avatar",2.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (3,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (4,"Avatar",3.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (5,"Avatar",2);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (6,"Avatar",3);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (7,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (1,"Avatar",5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (2,"Avatar",2.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (3,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (4,"Avatar",3.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (5,"Avatar",2);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (6,"Avatar",3);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (7,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (1,"Avatar",5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (2,"Avatar",2.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (3,"Avatar",4.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (4,"Avatar",3.5);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (5,"Avatar",2);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (6,"Avatar",3);
INSERT INTO movie_test(movie_id, movie_title, movie_rating) VALUES (7,"Avatar",4.5);
