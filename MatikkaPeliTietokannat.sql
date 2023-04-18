CREATE DATABASE mathgamedb;

CREATE TABLE Players(id INTEGER NOT NULL, username VARCHAR(40) NOT NULL UNIQUE, password VARCHAR(60) NOT NULL, PRIMARY KEY(id));

CREATE TABLE HighscoreAmounts(id INTEGER NOT NULL, playerId INTEGER NOT NULL, score INTEGER NOT NULL, PRIMARY KEY(id), FOREIGN KEY (playerId) REFERENCES Players(id));