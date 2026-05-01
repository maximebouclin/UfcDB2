Use UfcDB2;
-- QUERY 1
-- Height to weight ratio of orthodox fighters
SELECT fighter_name, fighter_height_inches/fighter_weight_lbs AS height_weight_ratio
	FROM fighter
    WHERE fighter_stance = 'Orthodox'
    ORDER BY height_weight_ratio DESC;

-- QUERY 2
-- Find all fighters who share teh same first and last name with another UFC fighter
SELECT f1.fighter_ID, f1.fighter_name
	FROM fighter f1 INNER JOIN fighter f2 
    ON (f1.fighter_name = f2.fighter_name AND NOT f1.fighter_ID = f2.fighter_ID)
    ORDER BY f1.fighter_name;

-- QUERY 3
-- Number of times each fighter has fought in a championship fight
SELECT fighter_name, COUNT(*) AS num_of_championship_fights
	FROM fight INNER JOIN fighter ON (fighter_ID = blue_fighter_ID OR fighter_ID = red_fighter_ID)
    WHERE is_championship_fight = TRUE
    GROUP BY fighter_name
    ORDER BY num_of_championship_fights DESC;
    
-- QUERY 4
-- Find all fighters who have won a fight and the number of fights they have won
SELECT fighter.fighter_name, COUNT(*) AS wins
	FROM fighter
	INNER JOIN (
		SELECT winner_ID
		FROM fight
	) AS winners ON (fighter.fighter_ID = winners.winner_ID)
	GROUP BY fighter.fighter_ID
	ORDER BY wins DESC;
    
-- QUERY 5 (Sequence of queries)
-- Create the view
DROP VIEW IF EXISTS fighter_stats;
CREATE VIEW fighter_stats AS
SELECT fighter.fighter_ID,
	fighter.fighter_name,
	fighter.fighter_stance,
	COUNT(fight.fight_ID) AS total_fights,
	SUM(IF(fight.winner_ID = fighter.fighter_ID, 1, 0)) AS wins,
    ROUND(SUM(IF(fight.winner_ID = fighter.fighter_ID, 1, 0)) / COUNT(fight.fight_ID) * 100, 2) AS win_percentage
FROM fighter
LEFT OUTER JOIN fight ON fighter.fighter_ID = fight.red_fighter_ID OR fighter.fighter_ID = fight.blue_fighter_ID
GROUP BY fighter.fighter_ID
ORDER BY total_fights DESC;

-- Show the current view
SELECT * FROM fighter_stats;