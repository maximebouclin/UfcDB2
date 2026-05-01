DROP DATABASE IF EXISTS UfcDB2;
CREATE DATABASE UfcDB2;
USE UfcDB2;

-- Create event table
DROP TABLE IF EXISTS event;
CREATE TABLE event (
	event_ID VARCHAR(100),
    event_name VARCHAR(200),
    event_location VARCHAR(100),
    event_date DATE,
    UNIQUE(event_name),
    PRIMARY KEY(event_ID)
);


-- Create fight table
DROP TABLE IF EXISTS fight;
CREATE TABLE fight (
	fight_ID VARCHAR(100),
    event_ID VARCHAR(100),
    red_fighter_ID VARCHAR(100),
    blue_fighter_ID VARCHAR(100),
    fight_weight_class_ID INT,
    winner_ID VARCHAR(100),
    outcome_method VARCHAR(50),
    round_ended INT CONSTRAINT valid_round CHECK(round_ended >=1 AND round_ended <= 5),
    is_championship_fight BOOLEAN,
    red_sig_strikes_landed INT,
    red_sig_strikes_attempted INT,
    red_takedowns_landed INT,
    red_takedowns_attempted INT,
    red_sub_attempts INT,
    red_control_secs INT,
	blue_sig_strikes_landed INT,
    blue_sig_strikes_attempted INT,
    blue_takedowns_landed INT,
    blue_takedowns_attempted INT,
    blue_sub_attempts INT,
    blue_control_secs INT,
    referee_name VARCHAR(100),
    PRIMARY KEY(fight_ID)
);


-- Create figher table
DROP TABLE IF EXISTS fighter;
CREATE TABLE fighter (
	fighter_ID VARCHAR(100),
    fighter_name VARCHAR(100),
    fighter_nickname VARCHAR(50),
    fighter_height_inches DECIMAL(5,2),
    fighter_weight_lbs DECIMAL(5,2),
    fighter_reach_inches DECIMAL(5,2),
    fighter_stance VARCHAR(30) CONSTRAINT valid_stance CHECK(fighter_stance IN ("Orthodox", "Southpaw", "Switch", "Sideways", "Open Stance")),
	fighter_DOB DATE,
    PRIMARY KEY(fighter_ID)
);


-- Create weight class table
DROP TABLE IF EXISTS weight_class;
CREATE TABLE weight_class (
	weight_class_ID INT AUTO_INCREMENT,
    weight_class_name VARCHAR(50),
    weight_class_limit_kg DECIMAL(5,2),
    UNIQUE(weight_class_name),
    PRIMARY KEY(weight_class_ID)
);

-- Add foreign keys to fight table
ALTER TABLE fight
	ADD FOREIGN KEY (event_ID) REFERENCES event(event_ID),
    ADD FOREIGN KEY (red_fighter_ID) REFERENCES fighter(fighter_ID),
    ADD FOREIGN KEY (blue_fighter_ID) REFERENCES fighter(fighter_ID),
    ADD FOREIGN KEY (fight_weight_class_ID) REFERENCES weight_class(weight_class_ID),
    ADD FOREIGN KEY (winner_ID) REFERENCES fighter(fighter_ID);

-- LOAD EVENT DATA
LOAD DATA LOCAL INFILE '/Users/maximebouclin/Projects/UfcDB2/data_files/event_info.csv'
INTO TABLE event
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

-- LOAD WEIGHT CLASS DATA
USE UfcDB2;

INSERT INTO weight_class (weight_class_name, weight_class_limit_kg)
	VALUES ("Flyweight", 56.7),
		("Bantamweight", 61.2),
        ("Featherweight", 65.8),
        ("Lightweight", 70.3),
        ("Welterweight", 77.1),
        ("Middleweight", 83.9),
        ("Light Heavyweight", 93.0),
        ("Heavyweight", 120.2),
        ("Women's Strawweight", 52.2),
        ("Women's Flyweight", 56.7),
        ("Women's Bantamweight", 61.2),
        ("Women's Featherweight", 65.8),
        ("Catch Weight", NULL),
        ("Open Weight", NULL);
        
-- LOAD FIGHTER DATA
LOAD DATA LOCAL INFILE '/Users/maximebouclin/Projects/UfcDB2/data_files/fighter_info.csv'
INTO TABLE fighter
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

-- LOAD FIGHT DATA
LOAD DATA LOCAL INFILE '/Users/maximebouclin/Projects/UfcDB2/data_files/fight_info.csv'
INTO TABLE fight
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(fight_ID,event_ID,red_fighter_ID,blue_fighter_ID,fight_weight_class_ID,winner_ID,outcome_method,round_ended,is_championship_fight,red_sig_strikes_landed,red_sig_strikes_attempted,red_takedowns_landed,red_takedowns_attempted,red_sub_attempts,red_control_secs,blue_sig_strikes_landed,blue_sig_strikes_attempted,blue_takedowns_landed,blue_takedowns_attempted,blue_sub_attempts,blue_control_secs,referee_name);
