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


