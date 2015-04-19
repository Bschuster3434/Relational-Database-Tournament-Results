Relational Database Tournament Results
by Brian Schuster
Created 4/16/15
Last Updated 4/16/15
-----------------------------------------------------------
PROJECT OUTLINE

A python application that keeps track of the results and
matches of a Swiss Style non-elimination tournament:

http://en.wikipedia.org/wiki/Swiss-system_tournament

The python application uses a PostgreSQL database to store
and maintain the data for the tournament. The python functions
describe how each function relates to running a tournament,
so document strings can be used to explain the various functions.

-----------------------------------------------------------
IMPORTANT FILES

STANDARD FROM PROJECT
- tournament.py
- tournament_test.py
- tournament.sql
- Database names 'tournament'

ADDITIONAL
- tournament_test_oddplayers.py (For testing use cases where byes are necessary)

-----------------------------------------------------------
TOOLS TO RUN CODE

- Python v2.7
- PostgreSQL Command Line Tool
- Vagrant
  - Please see instructions here for full install:
    https://www.udacity.com/wiki/ud197/install-vagrant
	(NOTE: If you follow the Vagrant Install, all tools will
	 be available on the VM)
	 
-----------------------------------------------------------
INSTRUCTIONS TO RUN TOURNAMENT TESTS

1) After going through the Vagrant tutorial, change your directory
to 'tournament'
2) Clone this git repository into the directory using:
	'git clone https://github.com/Bschuster3434/Relational-Database-Tournament-Results.git'
3) Once completed, type 'vagrant ssh' and use those credentials
   to SSH into your box
   - If you're on Windows 7, 'Putty' would work as your SSH client
4) Once in the virtual machine, change directories to :
   '/vagrant/tournament/tournamnet_results'
5) Run the two test scripts using the following commands:
   - python tournament_test.py
   - python tournament_test_oddplayers.py


