use tmdb;
#Query 1
SELECT m.title, k.`name`
FROM movie_metadata m
INNER JOIN movie_keywords mk ON m.tmdb_id = mk.tmdb_id
JOIN keywords k ON mk.keywords_id = k.keywords_id
WHERE k.`name` = 'Comedy';

#Query 2
SELECT m.title, AVG(r.rating) AS average_rating
FROM movie_metadata m
JOIN links l ON m.tmdb_id=l.tmdb_id
JOIN ratings r ON l.movie_id = r.movie_id GROUP BY m.title ORDER BY average_rating DESC;

#Query 3
SELECT mcr.tmdb_id,m.title,ca.cast_id,ca.name as Cast_name,ca.character_name,cr.id as crew_id,cr.name as crew_name,cr.department,cr.job FROM 
movie_crews mcr 
JOIN movie_casts mc on mcr.tmdb_id=mc.tmdb_id 
JOIN `casts` ca ON mc.credit_id=ca.credit_id
JOIN crews cr ON mcr.credit_id=cr.credit_id
JOIN links l ON l.tmdb_id=mcr.tmdb_id
JOIN movie_metadata m ON l.tmdb_id=m.tmdb_id where m.title="Ariel";

#Query 4
SELECT M.TMDB_ID AS MOVIE_ID,M.TITLE,MPC.production_companies_id,PC.`name`,C.production_countries_id,C.`name` FROM `movie_metadata` M 
JOIN `movie_production_companies` MPC ON M.TMDB_ID=MPC.TMDB_ID
JOIN `production_companies` PC ON MPC.production_companies_id=PC.production_companies_id
JOIN `movie_production_countries` MC ON M.TMDB_ID=MC.TMDB_ID
JOIN `production_countries` C ON MC.production_countries_id=C.production_countries_id order by  M.TMDB_ID ;


#Query 5
Select BC.name AS Collection_name, count(M.title) AS Number_of_Movies from `movie_belongs_to_collection` MBC 
JOIN movie_metadata M ON MBC.tmdb_id=M.tmdb_id
JOIN belongs_to_collection BC ON MBC.belongs_to_collection_id=BC.belongs_to_collection_id 
Group by BC.NAME having Number_of_Movies>10 order by Number_of_Movies;