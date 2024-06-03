SELECT current_club, AVG(age) AS age, AVG(goals_current_club) AS goals, AVG(appearances_current_club) AS apps
FROM players
WHERE current_club IS NOT NULL
GROUP BY current_club
ORDER BY age ASC;
