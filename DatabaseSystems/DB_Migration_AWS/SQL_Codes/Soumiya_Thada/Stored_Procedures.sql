-- Top 5 Collaborations of Director and Actors based on count

DROP PROCEDURE IF EXISTS display_top_collaborations;

DELIMITER //
CREATE PROCEDURE display_top_collaborations(IN director_name VARCHAR(255))
BEGIN
SELECT 
    casts.name AS 'Cast Name',
    GROUP_CONCAT(title) AS 'Collaborated Movies',
    COUNT(*) AS 'Total Number of Collaborations'
FROM
    casts
        JOIN
    movie_casts ON casts.credit_id = movie_casts.credit_id
        JOIN
    movie_crews ON movie_casts.tmdb_id = movie_crews.tmdb_id
        JOIN
    crews ON crews.credit_id = movie_crews.credit_id
        JOIN
    movie_metadata ON movie_metadata.tmdb_id = movie_crews.tmdb_id
WHERE
    crews.name = director_name
        AND department = 'Directing'
GROUP BY casts.name
ORDER BY COUNT(*) DESC
LIMIT 10;
END //

DELIMITER ;

CALL display_top_collaborations('Aki Kaurismäki');

-- Filter the movies by genre, release year and language

DROP PROCEDURE IF EXISTS filter_movie;

DELIMITER //

CREATE PROCEDURE filter_movie(IN genre_name VARCHAR(255), IN language_code VARCHAR(255), IN release_year YEAR, IN lim int)
BEGIN
SELECT 
    original_title AS 'Movie Title', release_date AS 'Release Date', overview AS 'Synopsis', runtime AS 'Runtime'
FROM
    movie_metadata
        JOIN
    movie_genres ON movie_genres.tmdb_id = movie_metadata.tmdb_id
        JOIN
    genres ON genres.genres_id = movie_genres.genres_id
WHERE
    genres.name = genre_name
        AND movie_metadata.original_language = language_code
        AND YEAR(movie_metadata.release_date) = release_year
ORDER BY popularity desc
LIMIT lim;
END //
DELIMITER ;

CALL filter_movie('Adventure', 'en', '2009', 5);

-- Check if a movie belongs to any collection

DROP PROCEDURE IF EXISTS check_if_belongs_to_collection;

DELIMITER //

CREATE PROCEDURE check_if_belongs_to_collection(IN movie_name VARCHAR(255))
BEGIN
	DECLARE collection_name VARCHAR(255);

    SELECT belongs_to_collection.name INTO collection_name
    FROM belongs_to_collection 
    INNER JOIN movie_belongs_to_collection  ON belongs_to_collection.belongs_to_collection_id = movie_belongs_to_collection.belongs_to_collection_id
    join movie_metadata on movie_belongs_to_collection.tmdb_id = movie_metadata.tmdb_id
    WHERE movie_metadata.title = movie_name;

    IF collection_name IS NOT NULL THEN
        SELECT CONCAT(movie_name, ' belongs to collection: ', collection_name) AS result;
    ELSE
        SELECT CONCAT(movie_name, ' does not belong to any collection') AS result;
    END IF;
END //

DELIMITER ;

CALL check_if_belongs_to_collection('Toy Story');
CALL check_if_belongs_to_collection('Jumanji');

-- Get Cast List for a movie

DROP PROCEDURE IF EXISTS display_cast_members;

DELIMITER //

CREATE PROCEDURE display_cast_members(IN movie_name VARCHAR(255))
BEGIN
SELECT 
    casts.name AS 'Cast Names'
FROM
    casts
        JOIN
    movie_casts ON casts.credit_id = movie_casts.credit_id
        JOIN
    movie_metadata ON movie_metadata.tmdb_id = movie_casts.tmdb_id
WHERE
    movie_metadata.title = movie_name
ORDER BY casts.order_num;
END //
DELIMITER ;

CALL display_cast_members('Jumanji');

