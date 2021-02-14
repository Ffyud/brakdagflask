## brakdagflask

Brakdagflask ontsluit het nieuwsarchief uit een database. Het nieuwsarchief bestaat uit nieuwsartikelen en bijbehorende bronnen.

---

* Brakdagflask is een rest-service gebouwd met het framework [Flask](https://flask.palletsprojects.com/). 
* De database bestaat uit een simpel [SQLLite](https://www.sqlite.org) oplossing, wat geen aparte server vereist. 
* In combinatie met [Gunicorn](https://gunicorn.org/) en [NGINX](https://www.nginx.com/) wordt de service beschikbaar via het web. 
* Met [Docker](https://www.docker.com/) wordt alles in de lucht gebracht. Er zijn twee containers nodig, één voor brakdagflask zelf en één voor NGINX.

---

### Draaien met Docker
----

1. Bouw het brakdagflask Docker image

`docker build -t brakdagflask:latest .`

2. Opstarten van de Docker container

`docker run --name brakdagflask -d -p 8000:5000 brakdagflask:latest`

3. Bouw het NGINX Docker image

`docker build -t nginx:latest .`

4. Opstarten van de Docker container

`docker run --name nginx -d -p 80:80 nginx:latest`

### Gebruik van de database
----
De database leeft als _.db_ bestand in het brakdagflask project. Het starten van de brakdagflask container maakt dus ook een lege nieuwe database aan.

Tabellen: 
* **Item** - voor het opslaan van artikelen
* **Bron** - voor het opslaan van bronnen

### Automatisch nieuws ophalen
----
Het **nieuws-ophalen** script bevraagd de _Bron_ tabel voor RSS-feeds en plaatst alle gevonden artikelen in de _Item_ tabel.

   
  

