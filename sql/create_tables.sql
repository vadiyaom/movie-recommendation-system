-- =============================================================================
-- Database Schema for Movie Recommendation System
-- Compatible with SQLite, PostgreSQL, and MySQL
-- =============================================================================

-- 1. Movies Table (Core Catalog)
CREATE TABLE IF NOT EXISTS movies (
    movie_id INT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    genres VARCHAR(255) NOT NULL,
    overview TEXT,
    keywords TEXT,
    cast TEXT,
    director VARCHAR(100),
    rating DECIMAL(3, 1),
    release_year INT,
    poster_url VARCHAR(500)
);

-- 2. Normalized Genres Lookup Table
CREATE TABLE IF NOT EXISTS genres (
    genre_id INT PRIMARY KEY,
    genre_name VARCHAR(50) NOT NULL UNIQUE
);

-- 3. Movie-Genre Junction Table (Many-to-Many Relationship)
CREATE TABLE IF NOT EXISTS movie_genres (
    movie_id INT,
    genre_id INT,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id) ON DELETE CASCADE
);

-- 4. User Search History Logging Table
CREATE TABLE IF NOT EXISTS search_history (
    search_id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_title VARCHAR(255) NOT NULL,
    searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    results_count INT DEFAULT 10
);

-- =============================================================================
-- Seed Data Insertion
-- =============================================================================

-- Populate Genres Lookup
INSERT INTO genres (genre_id, genre_name) VALUES
(1, 'Action'),
(2, 'Crime'),
(3, 'Drama'),
(4, 'Sci-Fi'),
(5, 'Adventure'),
(6, 'Thriller'),
(7, 'Mystery'),
(8, 'Animation'),
(9, 'Fantasy'),
(10, 'Romance')
ON CONFLICT(genre_id) DO NOTHING;

-- Populate Sample Movies Catalog
INSERT INTO movies (movie_id, title, genres, overview, keywords, cast, director, rating, release_year, poster_url) VALUES
(1, 'The Dark Knight', 'Action, Crime, Drama', 'When the menace known as the Joker wreaks havoc on Gotham, Batman must fight injustice.', 'batman dc comics joker gotham vigilante', 'Christian Bale, Heath Ledger, Aaron Eckhart', 'Christopher Nolan', 9.0, 2008, 'https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg'),
(2, 'Batman Begins', 'Action, Crime, Drama', 'Driven by tragedy, billionaire Bruce Wayne dedicates his life to fighting injustice in Gotham.', 'batman dc comics ninja gotham origin', 'Christian Bale, Michael Caine, Liam Neeson', 'Christopher Nolan', 8.2, 2005, 'https://image.tmdb.org/t/p/w500/1P3Gsl2daLwiv2jFvBfL1aK5Jk.jpg'),
(3, 'The Dark Knight Rises', 'Action, Crime, Thriller', 'Eight years after Joker, Batman must save Gotham from the brutal terrorist Bane.', 'batman dc comics bane catwoman gotham', 'Christian Bale, Tom Hardy, Anne Hathaway', 'Christopher Nolan', 8.4, 2012, 'https://image.tmdb.org/t/p/w500/hr0L2aueqlP2BYUblTTjmtn0hw4.jpg'),
(4, 'Inception', 'Action, Sci-Fi, Thriller', 'A thief who steals corporate secrets via dream-sharing is tasked with planting an idea.', 'dream subconscious inception heist mind', 'Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page', 'Christopher Nolan', 8.8, 2010, 'https://image.tmdb.org/t/p/w500/oYuLEt3zVCKq57qu2F8dT7NIa6f.jpg'),
(5, 'Interstellar', 'Adventure, Drama, Sci-Fi', 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity survival.', 'space exploration wormhole black hole time dilation', 'Matthew McConaughey, Anne Hathaway, Jessica Chastain', 'Christopher Nolan', 8.7, 2014, 'https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg'),
(6, 'Tenet', 'Action, Sci-Fi, Thriller', 'Armed with only one word, Tenet, a Protagonist journeys through a twilight world of espionage.', 'time inversion entropy spy temporal physics', 'John David Washington, Robert Pattinson, Elizabeth Debicki', 'Christopher Nolan', 7.3, 2020, 'https://image.tmdb.org/t/p/w500/k68nPLbIST6NP96JmTxmZijEvCA.jpg'),
(7, 'The Matrix', 'Action, Sci-Fi', 'A computer hacker learns from mysterious rebels about the true nature of his reality.', 'simulation virtual reality cyberpunk ai neo', 'Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss', 'Lana Wachowski', 8.7, 1999, 'https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg'),
(8, 'Gladiator', 'Action, Adventure, Drama', 'A former Roman General sets out to exact vengeance against the corrupt emperor.', 'ancient rome gladiator colosseum revenge maximus', 'Russell Crowe, Joaquin Phoenix, Connie Nielsen', 'Ridley Scott', 8.5, 2000, 'https://image.tmdb.org/t/p/w500/ty8TGRuvJLPUmAR1H1nRIsgwvim.jpg'),
(9, 'The Godfather', 'Crime, Drama', 'A chronicle of the Italian-American Corleone crime family under patriarch Vito Corleone.', 'mafia crime family organized crime mob don', 'Marlon Brando, Al Pacino, James Caan', 'Francis Ford Coppola', 9.2, 1972, 'https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg'),
(10, 'Pulp Fiction', 'Crime, Drama', 'The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales.', 'tarantino nonlinear hitman overdose dance dialogue', 'John Travolta, Uma Thurman, Samuel L. Jackson', 'Quentin Tarantino', 8.9, 1994, 'https://image.tmdb.org/t/p/w500/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg'),
(11, 'Spider-Man: Into the Spider-Verse', 'Animation, Action, Adventure', 'Teenager Miles Morales becomes Spider-Man and joins Spider-Heroes from parallel dimensions.', 'spider-man miles morales multiverse animated', 'Shameik Moore, Jake Johnson, Hailee Steinfeld', 'Bob Persichetti', 8.4, 2018, 'https://image.tmdb.org/t/p/w500/iiZZdoQBEYBv6id897TZZJ0C8xX.jpg'),
(12, 'Avatar', 'Action, Adventure, Fantasy, Sci-Fi', 'A paraplegic Marine dispatched to Pandora becomes torn between orders and protecting the Na vi.', 'alien planet pandora na vi colonization', 'Sam Worthington, Zoe Saldana, Sigourney Weaver', 'James Cameron', 7.9, 2009, 'https://image.tmdb.org/t/p/w500/kyeqWdyUXW608qlYkRqosgbbJyK.jpg')
ON CONFLICT(movie_id) DO NOTHING;

-- Populate Movie-Genre Mappings
INSERT INTO movie_genres (movie_id, genre_id) VALUES
(1, 1), (1, 2), (1, 3),    -- The Dark Knight (Action, Crime, Drama)
(2, 1), (2, 2), (2, 3),    -- Batman Begins (Action, Crime, Drama)
(3, 1), (3, 2), (3, 6),    -- The Dark Knight Rises (Action, Crime, Thriller)
(4, 1), (4, 4), (4, 6),    -- Inception (Action, Sci-Fi, Thriller)
(5, 5), (5, 3), (5, 4),    -- Interstellar (Adventure, Drama, Sci-Fi)
(6, 1), (6, 4), (6, 6),    -- Tenet (Action, Sci-Fi, Thriller)
(7, 1), (7, 4),            -- The Matrix (Action, Sci-Fi)
(8, 1), (8, 5), (8, 3),    -- Gladiator (Action, Adventure, Drama)
(9, 2), (9, 3),            -- The Godfather (Crime, Drama)
(10, 2), (10, 3),          -- Pulp Fiction (Crime, Drama)
(11, 8), (11, 1), (11, 5),  -- Spider-Verse (Animation, Action, Adventure)
(12, 1), (12, 5), (12, 4)   -- Avatar (Action, Adventure, Sci-Fi)
ON CONFLICT(movie_id, genre_id) DO NOTHING;

-- Seed Sample Search Logs
INSERT INTO search_history (movie_title, results_count) VALUES
('The Dark Knight', 10),
('Inception', 10),
('Interstellar', 10),
('The Dark Knight', 10),
('Avatar', 10),
('The Matrix', 10),
('Inception', 10);
