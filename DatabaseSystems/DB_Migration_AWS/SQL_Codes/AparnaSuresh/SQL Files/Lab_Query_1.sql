#Query 1:
SELECT m.title, k.name
FROM movie_metadata m
JOIN movie_keywords mk ON m.tmdb_id = mk.tmdb_id
JOIN KEYWORDS K ON MK.keywords_id = k.keywords_id
WHERE k.name = 'Comedy';

#Query 5:
Select BC.name AS Collection_name, count(m.title) AS Number_of_Movies from `movie_belongs_to_collection` MBC 
JOIN movie_metadata M ON MBC.tmdb_id=m.tmdb_id
JOIN belongs_to_collection BC ON MBC.belongs_to_collection_id=BC.belongs_to_collection_id 
Group by BC.NAME having Number_of_Movies>50 order by Number_of_Movies;

#Query 2:
SELECT m.title, AVG(r.rating) AS average_rating
FROM movie_metadata m
JOIN links l ON m.tmdb_id=l.tmdb_id
JOIN ratings r ON l.movie_id = r.movie_id GROUP BY m.title ORDER BY average_rating DESC;

#Query 3:
SELECT mcr.tmdb_id,m.title,ca.cast_id,ca.name as Cast_name,ca.character_name,cr.id as crew_id,cr.name as crew_name,cr.department,cr.job FROM 
movie_crews mcr 
JOIN movie_casts mc on mcr.tmdb_id=mc.tmdb_id 
JOIN `casts` ca ON mc.credit_id=ca.credit_id
JOIN crews cr ON mcr.credit_id=cr.credit_id
JOIN links l ON l.tmdb_id=mcr.tmdb_id
JOIN movie_metadata m ON l.tmdb_id=m.tmdb_id where m.title="Ariel";

#Query 4:
SELECT M.TMDB_ID AS MOVIE_ID,M.TITLE,MPC.production_companies_id,PC.`name`,C.production_countries_id,C.`name` FROM MOVIE_METADATA M 
JOIN MOVIE_PRODUCTION_COMPANIES MPC ON M.TMDB_ID=MPC.TMDB_ID
JOIN PRODUCTION_COMPANIES PC ON MPC.production_companies_id=PC.production_companies_id
JOIN MOVIE_PRODUCTION_COUNTRIES MC ON M.TMDB_ID=MC.TMDB_ID
JOIN PRODUCTION_COUNTRIES C ON MC.production_countries_id=C.production_countries_id order by  M.TMDB_ID ; 

select distinct (release_date) from movie_metadata order by release_date desc;
Select count(*) as Number_of_movies from movie_metadata where release_date like "%/%/35";
#STORED PROCEDURE 1
DELIMITER %%
CREATE procedure CountOfMovies_InYear(IN release_year VARCHAR(25),OUT Number_of_movies INT)
BEGIN
DECLARE search_pattern VARCHAR(255);
SET search_pattern = CONCAT('%/%/',release_year);
Select count(*) into Number_of_movies from movie_metadata where release_date like search_pattern;
END
%%

Call CountOfMovies_InYear(99, @number_of_movies);

Select @number_of_movies;
select * from movie_metadata  where release_date like "%/%/35";


#Stored Procedure 2
DELIMITER $$
CREATE PROCEDURE GetTopRatedMovies(
  IN `limit` INT,
  IN min_ratings INT
)
BEGIN
  SELECT m.title, AVG(r.rating) AS average_rating, COUNT(r.rating) AS rating_count
  FROM movie_metadata m
  INNER JOIN ratings r ON m.tmdb_id = r.movie_id
  GROUP BY m.title
  HAVING rating_count >= min_ratings
  ORDER BY average_rating DESC
  LIMIT `limit`;
END
$$
call GetTopRatedMovies(2,5);


#Trigger1
DELIMITER $$
CREATE TRIGGER enforce_unique_title_year
BEFORE INSERT ON movie_metadata
FOR EACH ROW
BEGIN
  DECLARE existing_movie INT;
  SELECT COUNT(*) INTO existing_movie
  FROM movie_metadata
  WHERE title = NEW.title AND release_date = NEW.release_date;
  IF existing_movie > 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Duplicate movie entry!';
  END IF;
END
$$
DELIMITER ;

DESCRIBE movie_metadata;
SELECT * FROM ratings;
INSERT INTO movie_metadata (tmdb_id,title,release_date) VALUES (2,"Ariel","10/21/88");

SHOW TRIGGERS;
#TRIGGER 2
DELIMITER $$
CREATE TRIGGER update_average_rating_log
AFTER INSERT ON ratings
FOR EACH ROW
BEGIN
  INSERT INTO movie_ratings (movie_id, rating_date, average_rating)
  VALUES (NEW.movie_id, CURDATE(), (
    SELECT AVG(rating) FROM ratings WHERE movie_id = NEW.movie_id
  ));
END
$$
CREATE TABLE movie_ratings(
movie_id INT,
rating_date DATE,
average_rating FLOAT
);
INSERT INTO ratings(user_id,movie_id,rating) values (1,2,5);
SELECT * from movie_ratings;

#TRIGGER 3:
DELIMITER $$
CREATE TRIGGER prevent_negative_rating
BEFORE INSERT ON ratings
FOR EACH ROW
BEGIN
  DECLARE rating_valid INT;
  SET rating_valid = (NEW.rating >= 0 AND NEW.rating <= 5);
  IF NOT rating_valid THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Rating must be between 0 and 5!';
  END IF;
END
$$

INSERT INTO ratings(user_id,movie_id,rating) values (1,2,-5);
