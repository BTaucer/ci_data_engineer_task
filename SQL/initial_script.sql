
CREATE TABLE players (
	id SERIAL PRIMARY KEY, 
	player_id VARCHAR(255),
	url VARCHAR(255) NOT NULL UNIQUE, 
	name VARCHAR(50),
	full_name VARCHAR(50),
	date_of_birth VARCHAR(50),
	age INTEGER,
	place_of_birth VARCHAR(50),
	country_of_birth VARCHAR(50),
	positions VARCHAR(50),
	current_club VARCHAR(50),
	national_team VARCHAR(50),
	appearances_current_club INTEGER,
	goals_current_club INTEGER, 
	scraping_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP 
);

GRANT USAGE, SELECT ON SEQUENCE players_id_seq TO korisnik;
GRANT CONNECT ON DATABASE c_and_i TO korisnik;
GRANT ALL ON SCHEMA public TO korisnik;
GRANT ALL PRIVILEGES ON players TO korisnik;