#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *

def testDeleteMatches():
    deleteByes()
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    deleteByes()
    deleteMatches()
    deletePlayers()
    print "2. Player records can be deleted."
	
def testDeleteBye():
	deleteByes()
	print "2a. Byes can be deleted."

def testCount():
    deleteByes()
    deleteMatches()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    deleteByes()
    deleteMatches()
    deletePlayers()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteByes()
    deleteMatches()
    deletePlayers()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteByes()
    deleteMatches()
    deletePlayers()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    standings = playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."


def testReportMatches():
    deleteByes() 
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."


def testByePairing():
    deleteByes()
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    registerPlayer("Magic Johnson")
    standings = playerStandings()
    [id1, id2, id3, id4, id5] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    reportMatch(id5)
    addByePlayer(id5)
    pairings = swissPairings()
    if len(pairings) != 3:
        raise ValueError(
            "For five players, swissPairings should return three pairs.")
	if len(pairings[0]) != 2:
	    raise ValueError(
		    "The first round must be the bye round, consisting of one player")
        print "First Pairing: " + string(pairings[0])
    print pairings
    if pairings[0][0] == id5:
        raise ValueError(
		    "The bye player must not be the same as a previous round")
    if pairings[0][0] in [id1, id3] and (pairings[1][0] != id5 and pairings[1][2] != id5):
        raise ValueError(
	        "Bye Player not properly placed.")
    elif pairings[0][0] in [id2, id4] and (pairings[2][0] != id5 and pairings[2][2] != id5):
        raise ValueError(
            "Bye Player not properly placed.")
    if bye_length != 2:
        raise ValueError(
            "After two rounds, there must be two players on the bye list")
    print "8. After one match, bye match is successfully implemented."
	


if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testByePairing()
    print "Success!  All tests pass!"


