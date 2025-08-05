-- 1. Movie Search Procedure: A stored procedure that accepts search criteria (such as genre, release date range, language) as input parameters and returns a result set of movies that match the criteria.

DELIMITER ##
create procedure MovieSearch (
    in p_genre VARCHAR(255),
    in p_release_date_start DATE,
    in p_release_date_end DATE,
    in p_language VARCHAR(255)
)
begin
    select *
    from movie_metadata inner join movie_genres on movie_metadata.tmdb_id = movie_genres.tmdb_id
    inner join genres on movie_genres.genres_id = genres.genres_id
    inner join movie_spoken_languages on movie_metadata.tmdb_id = movie_spoken_languages.tmdb_id
    inner join spoken_languages on movie_spoken_languages.spoken_languages_id = spoken_languages.spoken_languages_id
    where genres.name = p_genre
    and release_date between p_release_date_start and p_release_date_end
    and spoken_languages.spoken_languages_id = p_language;
end ##

-- call MovieSearch('Action', '2012-01-01', '2012-03-31', 'en');
  
-- 2. Calculate Movie Statistics Procedure: A stored procedure that calculates and returns statistics about movies, such as average rating, total revenue, etc.

DELIMITER ##
create procedure CalculateMovieStatistics()
begin
    select AVG(rating) as average_rating, SUM(revenue) as total_revenue
    from movie_metadata inner join links on links.tmdb_id = movie_metadata.tmdb_id
    inner join ratings on links.Movie_id = ratings.movie_id;
end ##

-- call CalculateMovieStatistics()

-- 3. Generate Movie Recommendations Procedure: A stored procedure that generates personalized movie recommendations for a user based on a specified genre.

DELIMITER ##
create procedure GenerateMovieRecommendations (
    in p_genre VARCHAR(255)
)
begin
    select movie_metadata.tmdb_id, title, AVG(rating) as average_rating
    from movie_metadata inner join links on links.tmdb_id = movie_metadata.tmdb_id
    inner join ratings on links.Movie_id = ratings.movie_id
    inner join movie_genres on movie_metadata.tmdb_id = movie_genres.tmdb_id
    inner join genres on movie_genres.genres_id = genres.genres_id
    where genres.name = p_genre
    group by ratings.movie_id
    order by average_rating desc
    limit 10;
end ##

-- call GenerateMovieRecommendations('Action');

-- 4. Log Search History Procedure: A stored procedure that logs user search queries into the search history table, capturing details such as search string, user ID, and timestamp.

DELIMITER ##
create procedure LogSearchHistory (
    in p_search_string VARCHAR(255),
    in p_user_id INT
)
begin
    insert into SearchHistory (search_string, user_id)
    values (p_search_string, p_user_id);
end ##

-- call LogSearchHistory("Search string", 1);

-- 5. Log View History Procedure: A stored procedure that logs user views of movies into the view history table, capturing details such as movie ID, user ID, and timestamp.
  
DELIMITER ##
create procedure LogViewHistory (
    in p_movie_id INT,
    in p_user_id INT
)
begin
    insert into ViewHistory (tmdb_id, user_id)
    values (p_movie_id, p_user_id);
end ##

-- call LogViewHistory(1, 1)
