call LogSearchHistory("Action", 1);
call LogSearchHistory("Ariel", 2);
call LogSearchHistory("Mickey", 3);
call LogViewHistory(2,2);

-- Introduce new collections
INSERT INTO belongs_to_collection (belongs_to_collection_id, name, poster_path, backdrop_path) VALUES
(1, 'Action Collection', '/poster.jpg', '/backdrop.jpg'),
(2, 'Romance Collection', '/poster.jpg', '/backdrop.jpg');

-- Update movie status after release
UPDATE movie_metadata SET status = 'Released' WHERE tmdb_id = 12345;

-- Retrieve all search history records for a specific user:
select * from SearchHistory where user_id = 123; -- Replace 123 with the actual user ID


-- Retrieve all view history records for a specific user:
select * from ViewHistory where user_id = 456; -- Replace 456 with the actual user ID

-- Delete all search history records older than 6 months:
delete from SearchHistory where search_date < DATE_SUB(NOW(), INTERVAL 6 MONTH);


-- Retrieve the top 10 users with the highest number of view history records:
select u.user_id, u.username, u.email, COUNT(vh.view_id) AS total_views from Users u left join ViewHistory vh on u.user_id = vh.user_id group by u.user_id order by total_views desc limit 10;
