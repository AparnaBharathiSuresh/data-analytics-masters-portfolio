
-- Trigger to Cascade Deletion:
DELIMITER ##
create trigger cascade_delete_movie_records after delete on movie_metadata
for each row
BEGIN
    delete links, ratings from ratings inner join links on ratings.movie_id = links.movie_id inner join movie_metadata on links.tmdb_id = movie_metadata.tmdb_id where links.tmdb_id = OLD.tmdb_id;
END;
##

-- Trigger to Enforce Budget Constraint
DELIMITER ##
create trigger enforce_budget_constraint before update on movie_metadata
for each row
BEGIN
    if NEW.budget < 45000 then
        signal sqlstate '45000'
        set message_text = 'Budget cannot be less than minimum threshold';
    end if;
END;
##
-- drop trigger enforce_budget_constraint
-- update movie_metadata set budget = 100 where tmdb_id = 2 

-- Trigger to update average rating of a movie when a new rating is inserted
DELIMITER ##
create trigger update_average_rating_trigger
after insert on ratings
for each row
BEGIN
    declare avg_rating FLOAT;
    declare total_rating FLOAT;
    declare total_users INT;
    
    select SUM(rating), COUNT(*) into total_rating, total_users from ratings where movie_id = NEW.movie_id;
    
    SET avg_rating = (total_rating * 2) / total_users;
    
    update movie_metadata inner join links on links.tmdb_id = movie_metadata.tmdb_id inner join ratings on ratings.movie_id = links.movie_id set vote_average = avg_rating where ratings.movie_id = NEW.movie_id;
END;
##

-- insert into ratings values (82, 4470, 5, NOW());
-- select * from movie_metadata where tmdb_id = 2;
