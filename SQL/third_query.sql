SELECT players.name, COUNT(players2.name)
	FROM players
	LEFT JOIN players AS players2
	ON players.positions = players2.positions
	AND players.age > players2.age
	AND players.appearances_current_club < players2.appearances_current_club
	WHERE players.current_club = 'Liverpool'
	GROUP BY (players.name);
