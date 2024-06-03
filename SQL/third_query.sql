SELECT players.name, count(players2.name) 
	FROM players
	LEFT JOIN players AS players2
	ON players.positions = players2.positions
	WHERE players.current_club = 'Liverpool' 
	AND players.age < players2.age 
	AND players.appearances_current_club > players2.appearances_current_club
	GROUP BY (players.name)