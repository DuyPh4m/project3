#!/bin/bash

# Set your Cassandra host and port
CASSANDRA_HOST=localhost
CASSANDRA_PORT=9042

# Set your keyspace and table name
KEYSPACE=MatchResults
TABLE=EPL1

# Create keyspace
echo "CREATE KEYSPACE IF NOT EXISTS $KEYSPACE WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 1};" | cqlsh $CASSANDRA_HOST $CASSANDRA_PORT

# Use keyspace
echo "USE $KEYSPACE;" | cqlsh $CASSANDRA_HOST $CASSANDRA_PORT

# Create table
echo "CREATE TABLE IF NOT EXISTS $KEYSPACE.$TABLE (id UUID PRIMARY KEY, Season text, DateTime text, HomeTeam text, AwayTeam text, FTHG int, FTAG int, FTR text, HTHG int, HTAG int, HTR text, Referee text, HS int, AS int, HST int, AST int, HC int, AC int, HF int, AF int, HY int, AY int, HR int, AR int);" | cqlsh $CASSANDRA_HOST $CASSANDRA_PORT

if [ $? -eq 0 ]
then
  echo "Cassandra setup successfully."
else
  echo "Cassandra setup failed."
  exit 1
fi