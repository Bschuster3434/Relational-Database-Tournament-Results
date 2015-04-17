#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
	"""Connect to the PostgreSQL database.  Returns a database connection."""
	return psycopg2.connect("dbname=tournament")

def deleteMatches():
	"""Remove all the match records from the database."""
	conn = connect()
	c = conn.cursor()
	c.execute("DELETE FROM match;")
	conn.commit()
	conn.close()


def deletePlayers():
	"""Remove all the player records from the database."""
	conn = connect()
	c = conn.cursor()
	c.execute("DELETE FROM registeredplayer;")
	conn.commit()
	conn.close()

def countPlayers():
	"""Returns the number of players currently registered."""
	conn = connect()
	c = conn.cursor()
	c.execute("SELECT COUNT(playerid) from registeredplayer;")
	player_count = c.fetchone()[0]
	return player_count
	


def registerPlayer(name):
	"""Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
	"""
	
	conn = connect()
	c = conn.cursor()
	c.execute("INSERT INTO registeredplayer (fullName) VALUES (%s);", (name,))
	conn.commit()
	conn.close()


def playerStandings():
	"""Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
	"""
	
	conn = connect()
	c = conn.cursor()
	
	# The Purpose of the below code is to do the following
	#  -At the lowest level subquery, we are calculating the number of wins by player
	#  -We are then matching that with the total number of matches played by player
	#  -Finally, we are joining that to the reg. player table to join the name
	# Wrapped match_info in case whens to return 0 when the value is null
	c.execute("""
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
	, CASE WHEN match_info.matches IS NULL THEN 0 ELSE match_info.matches END
""")
	current_standing = c.fetchall()
	return current_standing


def reportMatch(winner, loser):
	"""Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
	"""
	conn = connect()
	c = conn.cursor()
	c.execute("""
	INSERT INTO match (playerId, result) VALUES
		(%s, 'W'),
		(%s, 'L');""", (winner, loser,))
	conn.commit()
	conn.close()
 
def swissPairings():
	"""Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
	"""
	# Go get the current standings
	current_standings = playerStandings()
	
	# Based on the length of the standings, go through the list two at a time
	# Then append to the list 'next_round'
	next_round = []
	for match_create in range((len(current_standings)/2)):
		player_seed = match_create * 2 #Seed Refers to the relative importance of the match
		player_1 = current_standings[player_seed] #In first round, this equals the top player
		player_2 = current_standings[player_seed+1] #In the first round, this equals the 2nd top player
		next_match = player_1[:2] + player_2[:2] #returns the id and name of the two players
		next_round.append(next_match)
	
	return next_round
		
		
	
	


