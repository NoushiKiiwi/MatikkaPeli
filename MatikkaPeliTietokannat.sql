CREATE DATABASE mathgamedb;

CREATE TABLE Players(
    id INTEGER PRIMARY KEY, 
    username VARCHAR(40) NOT NULL UNIQUE, 
    password VARCHAR(60) NOT NULL);

CREATE TABLE ScoreAmounts(
    id INTEGER PRIMARY KEY, 
    playerId INTEGER NOT NULL, 
    score INTEGER NOT NULL, 
    gameMode VARCHAR(10), 
    FOREIGN KEY (playerId) REFERENCES Players(id));

CREATE TABLE ScoreTimed(
    id INTEGER PRIMARY KEY, 
    playerId INTEGER NOT NULL, 
    score INTEGER NOT NULL, 
    gameMode VARCHAR(10), 
    seconds INTEGER, 
    FOREIGN KEY (playerId) REFERENCES Players(id));
