CREATE DATABASE TMDB;

USE TMDB;

select * from BELONGS_TO_COLLECTION;

select * from GENREs;

select * from movie_BELONGS_TO_COLLECTION;

select * from MOVIE_GENRES;

select * from MOVIE_METADATA;

select * from movie_production_companies;

SELECT * FROM `movie_production_countries`;

SELECT * FROM `production_countries`;

SELECT * FROM `production_companies`;

SELECT * FROM movie_keywords order by id,tmdb_id;

select * from movie_keywords;

SELECT * FROM `movie_belongs_to_collection`;

(select m.tmdb_id from movie_metadata m);
select distinct(tmdb_id) from movie_keywords order by tmdb_id;

ALTER TABLE movie_keywords
ADD CONSTRAINT fk_tmdb_id FOREIGN KEY (tmdb_id) REFERENCES movie_metadata(tmdb_id);

select * from `credits_cast`;

SELECT cr.movie_id,m.title, cr.crew_id,cr.`name` AS crew_name, cr.job, cr.department,cc.cast_id,cc.`name`,cc.`character` AS character_name
FROM credits_crew cr 
JOIN credits_cast cc ON cr.movie_id=cc.movie_id
JOIN links l ON l.movie_id=cr.movie_id
JOIN movie_metadata m ON l.tmdb_id=m.tmdb_id
WHERE cr.movie_id IS NOT NULL ORDER BY cr.movie_id;

SELECT * FROM LINKS;

select * from credits_crew where movie_id is not null order by movie_id;

#Find all comedy movies

SELECT m.title, k.keyword_name
FROM movie_metadata m
INNER JOIN movie_keywords mk ON m.tmdb_id = mk.tmdb_id
JOIN KEYWORDS K ON MK.keyword_id = k.keyword_id
WHERE k.keyword_name = 'Comedy';

Select M.TMDB_ID AS Movie_id,M.title,BC.belongs_to_collection_id,BC.name  from `movie_belongs_to_collection` MBC 
JOIN movie_metadata M ON MBC.tmdb_id=m.tmdb_id
JOIN belongs_to_collection BC ON MBC.belongs_to_collection_id=BC.belongs_to_collection_id 
Group by BC.NAME;

Select BC.name AS Collection_name, count(m.title) AS Number_of_Movies from `movie_belongs_to_collection` MBC 
JOIN movie_metadata M ON MBC.tmdb_id=m.tmdb_id
JOIN belongs_to_collection BC ON MBC.belongs_to_collection_id=BC.belongs_to_collection_id 
Group by BC.NAME having Number_of_Movies>50 order by Number_of_Movies;

SELECT m.title, AVG(r.rating) AS average_rating
FROM movie_metadata m
JOIN links l ON m.tmdb_id=l.tmdb_id
JOIN ratings r ON l.movie_id = r.movie_id GROUP BY m.title ORDER BY average_rating DESC;

select * from links;

use tmdb1;


SELECT M.TMDB_ID AS MOVIE_ID,M.TITLE,MPC.production_companies_id,PC.`name`,C.production_countries_id,C.`name` FROM MOVIE_METADATA M 
JOIN MOVIE_PRODUCTION_COMPANIES MPC ON M.TMDB_ID=MPC.TMDB_ID
JOIN PRODUCTION_COMPANIES PC ON MPC.production_companies_id=PC.production_companies_id
JOIN MOVIE_PRODUCTION_COUNTRIES MC ON M.TMDB_ID=MC.TMDB_ID
JOIN PRODUCTION_COUNTRIES C ON MC.production_countries_id=C.production_countries_id; 