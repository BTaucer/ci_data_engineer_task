ALTER TABLE players
ADD COLUMN AgeCategory VARCHAR(10);

UPDATE players
SET AgeCategory =
	CASE WHEN age <= 23 THEN 'young'
		WHEN age >= 24 AND age <=32 THEN 'MidAge'
		WHEN age>=33 THEN 'old'
		ELSE NULL
	END;

ALTER TABLE players
ADD COLUMN GoalsPerClubGame NUMERIC;

UPDATE players
SET GoalsPerClubGame = 
	CASE WHEN appearances_current_club > 0 THEN CAST(goals_current_club AS NUMERIC)/appearances_current_club
		ELSE NULL
	END;

