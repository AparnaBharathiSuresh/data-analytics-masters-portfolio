-- Top 10 movies based on revenue generated

SELECT 
    original_title AS 'Movie Title',
    FORMAT(budget / 1000000, 2) AS 'Budget in Millions',
    FORMAT(revenue / 1000000, 2) AS 'Revenue in Millions',
    FORMAT((revenue - budget) / 1000000, 2) AS 'Profit in Millions'
FROM
    movie_metadata
ORDER BY revenue DESC
LIMIT 10;

-- Number of Movies in each genre

SELECT 
    genres.name AS 'Genres', COUNT(*) AS 'Movies Count'
FROM
    movie_genres
        JOIN
    genres ON genres.genres_id = movie_genres.genres_id
GROUP BY movie_genres.genres_id;

-- Top 5 movies based on Popularity score in each genre

WITH RankedMovies AS (
    SELECT
        genres.name,
        movie_metadata.title,
        ROW_NUMBER() OVER(PARTITION BY movie_genres.genres_id ORDER BY movie_metadata.popularity DESC) AS genre_rank
    FROM
        movie_genres 
    JOIN
        movie_metadata  ON movie_metadata.tmdb_id = movie_genres.tmdb_id
	JOIN 
       genres on genres.genres_id = movie_genres.genres_id
)
SELECT
	genre_rank AS 'Popularity Rank',
    name AS 'Genres',
    title AS 'Movie name'
FROM
    RankedMovies
WHERE
    genre_rank <= 5;

-- Top 15 Keywords

SELECT 
    keywords.name AS 'Top 15 Keywords'
FROM
    movie_keywords
        JOIN
    keywords ON keywords.keywords_id = movie_keywords.keywords_id
GROUP BY movie_keywords.keywords_id
ORDER BY COUNT(*) DESC
LIMIT 15;

-- Weighted Rating based on Number of Votes and Vote Average
SELECT 
    original_title AS 'Movie',
    vote_average,
    vote_count,
    ((vote_average * vote_count) + ((SELECT 
            AVG(vote_average)
        FROM
            movie_metadata) * 109)) / (vote_count + 109) AS weighted_rating
FROM
    movie_metadata
ORDER BY weighted_rating DESC
LIMIT 5;




