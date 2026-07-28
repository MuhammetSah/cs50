-- 7. All movies and ratings from 2010, in decreasing order by rating (alphabetical for those with same rating)
SELECT movies.title, ratings.rating FROM movies, ratings
WHERE movies.id = ratings.movie_id AND movies.year = 2010
ORDER BY ratings.rating DESC, movies.title ASC;
