-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE tournament (
tournamentId serial Primary Key,
tournamentName text);

CREATE TABLE registeredPlayer (
 playerId serial Primary Key,
 fullName text,
 tournament serial references tournament(tournamentId));
 
CREATE TABLE match (
matchId serial Primary Key,
playerId serial references registeredPlayer(playerId),
tournamentId serial references tournament(tournamentId),
round int,
result text);


