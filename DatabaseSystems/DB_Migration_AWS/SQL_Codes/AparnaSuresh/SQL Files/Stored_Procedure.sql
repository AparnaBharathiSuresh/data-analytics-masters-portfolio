#Procedure 1
DELIMITER %%
CREATE procedure CountOfMovies_InYear(IN release_year VARCHAR(25),OUT Number_of_movies INT)
BEGIN
DECLARE search_pattern VARCHAR(255);
SET search_pattern = CONCAT(release_year,"-%-%");
Select count(*) into Number_of_movies from movie_metadata where release_date like search_pattern;
END
%%
DROP procedure CountOfMovies_InYear;
Call CountOfMovies_InYear(1999, @number_of_movies);
Select @number_of_movies; 

#Procedure 2
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
