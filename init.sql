USE Brakdag;

CREATE TABLE IF NOT EXISTS Bron (id INTEGER PRIMARY KEY AUTOINCREMENT, 
title TEXT, link_rss TEXT, logo TEXT, description TEXT, link_home TEXT);

CREATE TABLE IF NOT EXISTS Item (id INTEGER PRIMARY KEY AUTOINCREMENT, 
title TEXT, link TEXT, timestamp_publicatie INTEGER, 
timestamp_gevonden INTEGER, description TEXT, 
uitgelicht INTEGER, bron_id INTEGER);