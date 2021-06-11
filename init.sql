USE brakdag;

CREATE TABLE IF NOT EXISTS Bron (id INTEGER PRIMARY KEY AUTO_INCREMENT, 
title TEXT, link_rss TEXT, logo TEXT, description TEXT, link_home TEXT);

CREATE TABLE IF NOT EXISTS Item (id INTEGER PRIMARY KEY AUTO_INCREMENT, 
title TEXT, link TEXT, timestamp_publicatie INTEGER, 
timestamp_gevonden INTEGER, description TEXT, 
uitgelicht INTEGER, bron_id INTEGER);

CREATE TABLE IF NOT EXISTS Item_match (id INTEGER PRIMARY KEY AUTO_INCREMENT, 
item INTEGER, item_compare INTEGER, match_percentage INTEGER);

INSERT INTO Bron (title, link_rss, logo, description, link_home) VALUES ('RTV Noord','https://rtvnoord.nl/rss','logos/logo_rtvnoord.png','Het nieuws uit Groningen.','https://www.rtvnoord.nl');
INSERT INTO Bron (title, link_rss, logo, description, link_home) VALUES ('OOGtv','https://oogtv.nl/feed/rss','logos/logo_oog.png','De stadszender van Groningen.','https://www.oogtv.nl');
INSERT INTO Bron (title, link_rss, logo, description, link_home) VALUES ('Sikkom','https://sikkom.nl/rss','logos/logo_sikkom.png','Nieuws, uitgaan, zin en onzin in Groningen.','https://www.sikkom.nl');
INSERT INTO Bron (title, link_rss, logo, description, link_home) VALUES ('Groninger Internet Courant','https://www.gic.nl/startpagina/rss','logos/logo_gic.png','Voor Stad en Ommeland. De feiten die tellen. Sinds 1997.','https://www.gic.nl');
INSERT INTO Bron (title, link_rss, logo, description, link_home) VALUES ('NU.nl Groningen','https://www.nu.nl/rss/groningen','logos/logo_nu.png','Het laatste nieuws het eerst op NU.nl.','https://www.nu.nl');
INSERT INTO Bron (title, link_rss, logo, description, link_home) VALUES ('De Smaak van Stad','https://www.desmaakvanstad.nl/feed/','logos/logo_smaak.png','Alles over eten en drinken in Groningen.','https://www.desmaakvanstad.nl');
INSERT INTO Bron (title, link_rss, logo, description, link_home) VALUES ('Groninger Ondernemers Courant','https://www.groningerondernemerscourant.nl/nieuws/rss','logos/logo_groc.png','Voor ondernemers en door ondernemers.','https://www.groningerondernemerscourant.nl');
INSERT INTO Bron (title, link_rss, logo, description, link_home) VALUES ('Focus Groningen','https://www.focusgroningen.nl/feed/','logos/logo_focus.png','Alles over Groningen en meer.','https://www.focusgroningen.nl');
INSERT INTO Bron (title, link_rss, logo, description, link_home) VALUES ('Gemeente Groningen','https://gemeente.groningen.nl/rss-news.xml','logos/logo_gemeente.png','Algemeen nieuws van de gemeente.','https://gemeente.groningen.nl');
INSERT INTO Bron (title, link_rss, logo, description, link_home) VALUES ('indebuurt Groningen','https://indebuurt.nl/groningen/feed/','logos/logo_buurt.png','indebuurt inspireert en informeert inwoners van Groningen via nieuws, artikelen, aanbiedingen en tips over ontwikkelingen en activiteiten in de buurt.','https://indebuurt.nl');
INSERT INTO Bron (title, link_rss, logo, description, link_home) VALUES ('Campus Groningen','https://campus.groningen.nl/nieuws/rss','logos/logo_campus.png','De Campus is de innovatiemotor van Noord-Nederland.','https://campus.groningen.nl');
INSERT INTO Bron (title, link_rss, logo, description, link_home) VALUES ('Horeca Groningen','https://www.horecagroningen.nl/feed/','logos/logo_horeca.png','Partner van de Groningse Horeca.','https://www.horecagroningen.nl');
INSERT INTO Bron (title, link_rss, logo, description, link_home) VALUES ('Groningen Bereikbaar','https://www.groningenbereikbaar.nl/nieuws/rss','logos/logo_bereikbaar.png','Groningen Bereikbaar houdt de stad en regio, samen met vele partners, zo goed mogelijk bereikbaar en helpt reizigers slimmer te reizen.','https://www.groningenbereikbaar.nl');
INSERT INTO Bron (title, link_rss, logo, description, link_home) VALUES ('Stad Groningen Clickt','https://stadclickt.nl/feed','logos/logo_clickt.png','De stadblog van Groningen.','https://stadclickt.nl');
INSERT INTO Bron (title, link_rss, logo, description, link_home) VALUES ('DATmag','https://datmag.nl/feed/rss','logos/logo_datmag.png','Creatief talent en ondernemerschap in Groningen.','https://datmag.nl');
INSERT INTO Bron (title, link_rss, logo, description, link_home) VALUES ('Groninger Studentenkrant','https://studentenkrant.org/feed/','logos/logo_sk.png','De Groninger Studentenkrant is een onafhankelijk blad gemaakt voor en door studenten van HBO en WO-instellingen in Groningen.','https://studentenkrant.org');
INSERT INTO Bron (title, link_rss, logo, description, link_home) VALUES ('UKrant','https://www.ukrant.nl/feed','logos/logo_uk.png','Onafhankelijk nieuwsmedium voor academisch Groningen.','https://www.ukrant.nl');
INSERT INTO Bron (title, link_rss, logo, description, link_home) VALUES ('Eetbaar Groningen','https://eetbarestadgroningen.nl/category/nieuws/feed/rss','logos/logo_eetbare.png','Moestuinieren voor en door de buurt. Ondersteund door de Natuur en Milieufederatie en de Gemeente Groningen.','https://eetbaargroningen.nl');
INSERT INTO Bron (title, link_rss, logo, description, link_home) VALUES ('Filter groningen','https://www.filtergroningen.nl/feed/','logos/logo_filter.png','Filter Groningen selecteert cultuur, zodat jij weet wat er te beleven valt.','https://www.filtergroningen.nl');
INSERT INTO Bron (title, link_rss, logo, description, link_home) VALUES ('Groninger Krant','https://groningerkrant.nl/groningen/rss','logos/logo_groninger.png','De Groninger Krant brengt nieuws, tips en persoonlijke verhalen uit Groningen dichterbij.','https://groningerkrant.nl');
INSERT INTO Bron (title, link_rss, logo, description, link_home) VALUES ('JouwStad Groningen','https://jouwstad.eu/feed/','logos/logo_jouwstad.png','Nieuwsblog met dagelijks het nieuws uit de stad Groningen.','https://jouwstad.eu');
INSERT INTO Bron (title, link_rss, logo, description, link_home) VALUES ('Groningen Fietsstad','https://groningenfietsstad.nl/nieuws/feed/','logos/logo_fietsstad.png','Fiets, cultuur, inspiratie, dromen en de realiteit. Wij fietsen met veel, heel veel. Wij zijn Groningen Fietsstad.','https://groningenfietsstad.nl');
INSERT INTO Bron (title, link_rss, logo, description, link_home) VALUES ('HanzeMAG','http://www.hanzemag.nl/category/nieuws/feed/rss','logos/logo_hanzemag.png','Redactioneel onafhankelijk magazine van de Hanzehogeschool.','https://hanzemag.nl');
INSERT INTO Bron (title, link_rss, logo, description, link_home) VALUES ('POPgroningen','https://popgroningen.nl/nieuws/rss','logos/logo_pop.png','Popkoepel van provincie Groningen.','https://popgroningen.nl');
INSERT INTO Bron (title, link_rss, logo, description, link_home) VALUES ('Groningen Spoorzone','https://www.groningenspoorzone.nl/nieuws/rss','logos/logo_spoorzone.png','Met Groningen Spoorzone werken we aan de bereikbaarheid van Groningen.','https://www.groningenspoorzone.nl');
INSERT INTO Bron (title, link_rss, logo, description, link_home) VALUES ('OIS Groningen','https://oisgroningen.nl/feed/','logos/logo_os.png','Afdeling Onderzoek, Informatie en Statistiek Gemeente Groningen.','https://oisgroningen.nl');
INSERT INTO Bron (title, link_rss, logo, description, link_home) VALUES ('3voor12 Groningen','https://rs.vpro.nl/v3/api/feeds/3voor12/section/3voor12%20Groningen','logos/logo_paal.png','3voor12 groningen is de Groningse redactie van 3voor12, de muziektak van de VPRO.','https://3voor12.vpro.nl');
INSERT INTO Bron (title, link_rss, logo, description, link_home) VALUES ('Kunst en Stad','http://kunstenstad.nl/feed/','logos/logo_kunst.png','Kunst en Stad is een uitgave van het Centrum Beeldende Kunst Groningen.','http://kunstenstad.nl');
INSERT INTO Bron (title, link_rss, logo, description, link_home) VALUES ('Markten Groningen', 'https://marktengroningen.nl/nieuws/feed', 'logos/logo_markten.png', 'Een overzicht van al het nieuws op en over de Markten Groningen.', 'https://marktengroningen.nl');
