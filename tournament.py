#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import random


def connect():
	"""Connect to the PostgreSQL database.  Returns a database connection."""
	return psycopg2.connect("dbname=tournament")

def deleteMatches():
	"""Remove all the match records from the database.
	In addition to deleting matches, we are also going to
	be deleting from the 'playerBye' table, as these are
	the two tables that are most closely linked."""
	conn = connect()
	c = conn.cursor()
	c.execute("DELETE FROM match; DELETE FROM playerbye;")
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
	
def retrieveByes():
	"""Retrieves the list of players who have received byes."""
	conn = connect()
	c = conn.cursor()
	c.execute("SELECT playerid from playerbye;")
	players_with_byes_lot = c.fetchall() #List of tuples... let's change this!
	# Flattened List Below
	players_with_byes = [item for sublist in players_with_byes_lot for item in sublist]
	conn.close()
	return players_with_byes
	
def addByePlayer(playerId):
	"""Add a player to the 'bye' list."""
	conn = connect()
	c = conn.cursor()
	c.execute("INSERT INTO playerbye VALUES (%s);", (playerId,))
	conn.commit()
	conn.close()

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
	c.execute("SELECT * from playerstanding;")
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
	
	#Below if statement is looking for odd number of players in standings
	if (len(current_standings) % 2) != 0:
		players_with_byes = retrieveByes()
		bye_player = ()
		while bye_player == ():
			next_choice = random.choice(current_standings) #pick a random player
			if next_choice[0] not in players_with_byes: #If the players hasn't had a bye...
				next_round.append(next_choice[:2]) #Add him to 'next_round'
				current_standings.remove(next_choice) #Remove the player from current standing
				addByePlayer(next_choice[0]) #Add the playerId (value 0) to playerBye
				bye_player = next_choice #Change 'bye_player' flag so 'while' loop ends
	
	for match_create in range((len(current_standings)/2)):
		player_seed = match_create * 2 #Seed Refers to the relative importance of the match
		player_1 = current_standings[player_seed] #In first round, this equals the top player
		player_2 = current_standings[player_seed+1] #In the first round, this equals the 2nd top player
		next_match = player_1[:2] + player_2[:2] #returns the id and name of the two players
		next_round.append(next_match)
	
	return next_round
		
		
	
	


