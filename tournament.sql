-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

--Files to create the tables in the database 'tournament'

CREATE TABLE registeredPlayer (
 playerId serial Primary Key,
 fullName text);
 
CREATE TABLE match (
id serial Primary Key,
playerId serial references registeredPlayer(playerId),
result text);

-- The Purpose of the below code is to do the following
--  -At the lowest level subquery, we are calculating the number of wins by player
--  -We are then matching that with the total number of matches played by player
--  -Finally, we are joining that to the reg. player table to join the name
-- Wrapped match_info in case whens to return 0 when the value is null

CREATE VIEW playerStanding AS
	SELECT registeredplayer.playerid as id
	, registeredplayer.fullname as name
	, CASE WHEN match_info.wins IS NULL THEN 0 ELSE match_info.wins END as wins
	, CASE WHEN match_info.matches IS NULL THEN 0 ELSE match_info.matches END as matches
	from registeredplayer
	LEFT OUTER JOIN	
		(SELECT match.playerid
		, count(match.id) as matches
		, count(wins.wins) as wins
		FROM match
		LEFT OUTER JOIN 
			(SELECT playerid, count(id) as wins from match where result = 'W' group by playerid) as wins
		on match.playerid = wins.playerid
		group by match.playerid) as match_info 
	on registeredplayer.playerid = match_info.playerid
	ORDER BY CASE WHEN match_info.wins IS NULL THEN 0 ELSE match_info.wins END DESC
	, CASE WHEN match_info.matches IS NULL THEN 0 ELSE match_info.matches END;


