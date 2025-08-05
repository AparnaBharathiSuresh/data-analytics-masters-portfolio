CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) DEFAULT NULL,
    email VARCHAR(255) DEFAULT NULL,
    password VARCHAR(255) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE ratings ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES Users(USER_ID);

insert into Users(User_id) select distinct user_id from ratings;

CREATE TABLE SearchHistory (
    search_id INT PRIMARY KEY AUTO_INCREMENT,
    search_string VARCHAR(255),
    search_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) on delete cascade
);

CREATE TABLE ViewHistory (
    view_id INT PRIMARY KEY AUTO_INCREMENT,
    tmdb_id INT,
    view_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) on delete cascade
);


CREATE VIEW movie_details AS
SELECT mm.*, mbc.belongs_to_collection_id, mg.genre_id, mk.keyword_id
FROM movie_metadata AS mm
JOIN movie_belongs_to_collection AS mbc ON mm.tmdb_id = mbc.tmdb_id
JOIN movie_genres AS mg ON mm.tmdb_id = mg.tmdb_id
JOIN movie_keywords AS mk ON mm.tmdb_id = mk.tmdb_id;



CREATE USER 'viewro'@'%' IDENTIFIED BY 'tmdb';

GRANT SELECT ON tmdb.movie_details TO 'viewro'@'%';

FLUSH PRIVILEGES;



CREATE USER 'ltdrw'@'%' IDENTIFIED BY 'tmdb';

GRANT SELECT ON tmdb.* TO 'ltdrw'@'%';

GRANT INSERT, UPDATE, DELETE ON tmdb.ratings TO 'ltdrw'@'%';
GRANT INSERT, UPDATE, DELETE ON tmdb.Users TO 'ltdrw'@'%';
GRANT INSERT, UPDATE, DELETE ON tmdb.ViewHistory TO 'ltdrw'@'%';
GRANT INSERT, UPDATE, DELETE ON tmdb.SearchHistory TO 'ltdrw'@'%';

FLUSH PRIVILEGES;
