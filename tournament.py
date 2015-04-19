#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import random

def connect():
	return psycopg2.connect("dbname=tournament")

def connect_execute(sql):
    """Connect to the PostgreSQL database and runs the SQL statement.
       Based on the sql_type, it will either run the sql and return nothing,
       or return the result of the select statement.
    """
    # Grabbing the SQL Command based off of first word
    # If function is string, just split and look at the first item
    # If tuple, pull out the statement, then split it
    if type(sql) is tuple:
        sql_type = sql[0].split(" ")[0].lower()
    elif isinstance(sql, basestring):
        sql_type = sql.split(" ")[0].lower()
    else:
        raise ValueError(
            "SQL statement is not tuple or string. SQL Type is: " + str(type(sql)))
    # If the sql_type not one of the three statements, print this error
    if sql_type not in ['select', 'insert', 'delete']:
        raise ValueError("sql_type must be 'select', 'insert' or 'delete'")
    
    conn = psycopg2.connect("dbname=tournament")
    c = conn.cursor()
    
    # If the SQL type is 'insert' or 'delete', we need to check if the sql has any
    # formatting strings, which we can figure out if the type is a tuple
    if sql_type in ['insert', 'delete']:
        if type(sql) is not tuple:
            c.execute(sql) # Breaking up cursor object to be read by 'execute' statement
        else:
            c.execute(sql[0],sql[1])
        conn.commit()
        conn.close()
    else:
        c.execute(sql)
        result = c.fetchall()
        conn.close()
        return result

def deleteMatches():
    """Remove all the match records from the database."""
    connect_execute("DELETE FROM match;")
	
def deleteByes():
    """Remove all the byes stored in the Database."""
    connect_execute("DELETE FROM playerbye;")

def deletePastMatches():
    """Delete Past Matches from the schema."""
    connect_execute("DELETE FROM pastmatch;")

def deletePlayers():
    """Remove all the player records from the database."""
    connect_execute("DELETE FROM registeredplayer;")

def countPlayers():
    """Returns the number of players currently registered."""
    player_count = connect_execute("SELECT COUNT(playerid) from registeredplayer;")
    player_count = player_count[0][0]
    return player_count
	
def retrieveByes():
    """Retrieves the list of players who have received byes."""
    players_with_byes_lot = connect_execute("SELECT playerid from playerbye;") 
    # players_with_byes_lot is a List of tuples... let's change this!
    # Flattened List Below
    players_with_byes = [item for sublist in players_with_byes_lot for item in sublist]
    return players_with_byes
	
def addByePlayer(playerId):
    """Add a player to the 'bye' list."""
    cursor_object = "INSERT INTO playerbye (playerid) VALUES (%s);",(playerId,)
    connect_execute(cursor_object)
	
def countByePlayer():
    """Returns players on 'bye' list."""
    result = connect_execute("SELECT * FROM playerbye;")
    return result

def addMatchPlayers(playerOne, playerTwo):
    """Add a new match to pastmatch"""
    cursor_object = "INSERT INTO pastmatch (playeridone, playeridtwo) VALUES (%s,%s)", (playerOne, playerTwo,)
    connect_execute(cursor_object)

def retrievePastMatches():
    """Retrieves the list of past player matches including the inverse
       of every match
    """
    result_list = connect_execute("SELECT playeridone, playeridtwo from pastmatch")
    result_list_with_inverse = []
    for match in result_list:
        result_list_with_inverse.append(match)
        match_inverse = (match[1], match[0])
        result_list_with_inverse.append(match_inverse)
    return result_list_with_inverse
       

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    cursor_object = "INSERT INTO registeredplayer (fullName) VALUES (%s)",(name,)
    connect_execute(cursor_object)


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
	
	current_standing = connect_execute("SELECT id, name, wins, matches from playerstanding;")
	return current_standing


def reportMatch(winner, loser = None):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
	"""
    if loser == None:
        statement = "INSERT INTO match (playerId, result) VALUES (%s, 'W');",(winner,)		
    else:
        statement = "INSERT INTO match (playerId, result) VALUES(%s, 'W'),(%s, 'L');",(winner, loser,)
    connect_execute(statement)
 
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

    past_matches = retrievePastMatches()
	
	for match_create in range((len(current_standings)/2)):
		player_seed = match_create * 2 #Seed Refers to the relative importance of the match
		player_1 = current_standings[player_seed] #In first round, this equals the top player
		player_2 = current_standings[player_seed+1] #In the first round, this equals the 2nd top player
		next_match = player_1[:2] + player_2[:2] #returns the id and name of the two players
		next_round.append(next_match)
	
	return next_round
		
		
	
	


