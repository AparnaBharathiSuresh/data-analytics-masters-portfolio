#Trigger 1
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

SELECT * FROM movie_metadata;

INSERT INTO movie_metadata (tmdb_id,title,release_date) VALUES (2,"Ariel","1988-10-21")

#Trigger 2
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

SELECT * FROM movie_ratings;

#Trigger 3
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
