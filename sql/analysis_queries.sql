-- =============================================================================
-- Movie Recommendation System - SQL Data Analysis Queries
-- Author: Om Vadiya (GitHub: @vadiyaom)
-- Database Engine Compatibility: SQLite, PostgreSQL, MySQL
-- Description: Analytical SQL queries demonstrating real-world Data Science
--              data extraction, aggregation, multi-table joins, subqueries,
--              and Common Table Expressions (CTEs).
-- =============================================================================

-- =============================================================================
-- SECTION 1: BASIC FILTERING, PROJECTION & SORTING
-- Concepts: SELECT, WHERE, AND/OR, ORDER BY, LIMIT
-- =============================================================================

-- Query 1: Top-Rated Modern Blockbusters
-- Business Question: What are the critically acclaimed movies (rating >= 8.5) 
-- released from the year 2000 onwards, ordered by highest rating first?
-- Interview Concept: Basic filtering with numerical conditions and sorting.
SELECT 
    title,
    release_year,
    director,
    rating,
    genres
FROM 
    movies
WHERE 
    release_year >= 2000 
    AND rating >= 8.5
ORDER BY 
    rating DESC, 
    release_year DESC;


-- Query 2: Catalog Search by Genre Keyword
-- Business Question: Which movies belong to the 'Sci-Fi' genre, ordered chronologically?
-- Interview Concept: Text pattern matching using the LIKE wildcard operator.
SELECT 
    movie_id,
    title,
    release_year,
    director,
    rating
FROM 
    movies
WHERE 
    genres LIKE '%Sci-Fi%'
ORDER BY 
    release_year ASC;


-- =============================================================================
-- SECTION 2: AGGREGATE FUNCTIONS & METRICS CALCULATION
-- Concepts: COUNT, AVG, MIN, MAX, ROUND
-- =============================================================================

-- Query 3: Overall Catalog Summary Statistics
-- Business Question: What is the total movie count, average IMDb rating, 
-- minimum rating, maximum rating, and release span of the current catalog?
-- Interview Concept: Portfolio-level summary KPI aggregations.
SELECT 
    COUNT(*) AS total_movies,
    ROUND(AVG(rating), 2) AS average_rating,
    MIN(rating) AS lowest_rating,
    MAX(rating) AS highest_rating,
    MIN(release_year) AS earliest_year,
    MAX(release_year) AS latest_year
FROM 
    movies;


-- =============================================================================
-- SECTION 3: GROUPING, AGGREGATION & FILTERING AGGREGATES
-- Concepts: GROUP BY, HAVING, Aggregate Functions
-- =============================================================================

-- Query 4: Director Performance Analytics (Minimum 2 Movies)
-- Business Question: Which directors have directed multiple movies in our catalog,
-- what is their film count, and what is their average rating?
-- Interview Concept: GROUP BY with HAVING filter on aggregated count, ORDER BY aggregate.
SELECT 
    director,
    COUNT(*) AS total_films,
    ROUND(AVG(rating), 2) AS avg_director_rating,
    MIN(release_year) AS first_film_year,
    MAX(release_year) AS latest_film_year
FROM 
    movies
GROUP BY 
    director
HAVING 
    COUNT(*) >= 2
ORDER BY 
    avg_director_rating DESC,
    total_films DESC;


-- Query 5: Decade-wise Release Distribution
-- Business Question: How many movies were released in each decade, and what was
-- the average rating per decade?
-- Interview Concept: Computed column grouping using integer division / floor math.
SELECT 
    (release_year / 10) * 10 AS decade,
    COUNT(*) AS movies_count,
    ROUND(AVG(rating), 2) AS avg_decade_rating
FROM 
    movies
GROUP BY 
    (release_year / 10) * 10
ORDER BY 
    decade ASC;


-- =============================================================================
-- SECTION 4: MULTI-TABLE RELATIONAL JOINS
-- Concepts: INNER JOIN, LEFT JOIN, Junction Tables, Many-to-Many Relationships
-- =============================================================================

-- Query 6: Genre-Level Movie Distribution & Average Rating
-- Business Question: What is the distribution of movies across normalized genres,
-- and what is the average audience rating for each genre?
-- Interview Concept: Multi-table INNER JOIN across normalized relational schema 
-- (movies -> movie_genres -> genres).
SELECT 
    g.genre_id,
    g.genre_name,
    COUNT(mg.movie_id) AS total_movies_in_genre,
    ROUND(AVG(m.rating), 2) AS avg_genre_rating
FROM 
    genres g
INNER JOIN 
    movie_genres mg ON g.genre_id = mg.genre_id
INNER JOIN 
    movies m ON mg.movie_id = m.movie_id
GROUP BY 
    g.genre_id, 
    g.genre_name
ORDER BY 
    total_movies_in_genre DESC,
    avg_genre_rating DESC;


-- Query 7: Detailed Movie Breakdown with Normalized Genres List
-- Business Question: List each movie alongside all normalized genres linked to it.
-- Interview Concept: Multi-table JOIN with GROUP_CONCAT / STRING_AGG aggregation.
SELECT 
    m.movie_id,
    m.title,
    m.director,
    m.rating,
    GROUP_CONCAT(g.genre_name, ', ') AS assigned_genres
FROM 
    movies m
LEFT JOIN 
    movie_genres mg ON m.movie_id = mg.movie_id
LEFT JOIN 
    genres g ON mg.genre_id = g.genre_id
GROUP BY 
    m.movie_id, 
    m.title, 
    m.director, 
    m.rating
ORDER BY 
    m.rating DESC;


-- =============================================================================
-- SECTION 5: SUBQUERIES (UNCORRELATED & CORRELATED)
-- Concepts: Scalar Subquery, Correlated Subquery, IN Operator
-- =============================================================================

-- Query 8: Movies Performing Above the Global Catalog Average Rating
-- Business Question: Which movies have an IMDb rating strictly higher than 
-- the catalog's overall average rating?
-- Interview Concept: Uncorrelated scalar subquery inside WHERE clause.
SELECT 
    movie_id,
    title,
    director,
    rating,
    ROUND(rating - (SELECT AVG(rating) FROM movies), 2) AS rating_delta_vs_mean
FROM 
    movies
WHERE 
    rating > (SELECT AVG(rating) FROM movies)
ORDER BY 
    rating DESC;


-- Query 9: Directors Whose Average Rating Exceeds Overall Catalog Average
-- Business Question: Find all movies directed by creators whose overall personal
-- filmography average is greater than 8.3.
-- Interview Concept: Subquery utilizing IN operator combined with GROUP BY / HAVING.
SELECT 
    title,
    director,
    rating,
    release_year
FROM 
    movies
WHERE 
    director IN (
        SELECT 
            director
        FROM 
            movies
        GROUP BY 
            director
        HAVING 
            AVG(rating) > 8.3
    )
ORDER BY 
    director ASC, 
    rating DESC;


-- =============================================================================
-- SECTION 6: COMMON TABLE EXPRESSIONS (CTEs) & ADVANCED ANALYTICS
-- Concepts: WITH Clause, Multi-step Data Transformation, Window Ranking
-- =============================================================================

-- Query 10: Top Performing Movie Per Normalized Genre Using CTE & Window Ranking
-- Business Question: For every genre, which film holds the number one rank by rating?
-- Interview Concept: Modular CTE pipeline with DENSE_RANK() / ROW_NUMBER() window function.
WITH RankedGenreMovies AS (
    SELECT 
        g.genre_name,
        m.title,
        m.director,
        m.rating,
        m.release_year,
        DENSE_RANK() OVER (
            PARTITION BY g.genre_name 
            ORDER BY m.rating DESC, m.release_year DESC
        ) AS rank_within_genre
    FROM 
        genres g
    INNER JOIN 
        movie_genres mg ON g.genre_id = mg.genre_id
    INNER JOIN 
        movies m ON mg.movie_id = m.movie_id
)
SELECT 
    genre_name,
    title AS top_movie,
    director,
    rating,
    release_year
FROM 
    RankedGenreMovies
WHERE 
    rank_within_genre = 1
ORDER BY 
    rating DESC, 
    genre_name ASC;


-- Query 11: Search Demand vs Catalog Rating Analysis
-- Business Question: How frequently was each title queried in the recommendation system,
-- and does user search interest correlate with high movie ratings?
-- Interview Concept: CTE aggregating search logs joined with movies catalog.
WITH SearchPopularity AS (
    SELECT 
        movie_title,
        COUNT(*) AS total_searches,
        MAX(searched_at) AS most_recent_search
    FROM 
        search_history
    GROUP BY 
        movie_title
)
SELECT 
    m.title,
    m.director,
    m.rating,
    COALESCE(sp.total_searches, 0) AS total_search_frequency,
    sp.most_recent_search
FROM 
    movies m
LEFT JOIN 
    SearchPopularity sp ON LOWER(m.title) = LOWER(sp.movie_title)
ORDER BY 
    total_search_frequency DESC, 
    m.rating DESC;
