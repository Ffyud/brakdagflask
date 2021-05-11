## brakdagflask

Brakdagflask ontsluit het nieuwsarchief uit een database. Het nieuwsarchief bestaat uit nieuwsartikelen en bijbehorende bronnen.

---

* Brakdagflask is een rest-service gebouwd met het framework [Flask](https://flask.palletsprojects.com/). 
* In combinatie met [Gunicorn](https://gunicorn.org/) en [NGINX](https://www.nginx.com/) wordt de service beschikbaar via het web. 
* Met [Docker](https://www.docker.com/) wordt alles in de lucht gebracht.

### Draaien met Docker Compose

`docker-compose up`

### Draaien met Docker

- Bouw het brakdagflask image

`docker build -t brakdagflask:latest .`

- Opstarten van de brakdagflask container

`docker run --name brakdagflask -d -p 8000:5000 brakdagflask:latest`

- Bouw het NGINX image

`docker build -t nginx:latest .`

- Opstarten van de NGINX container

`docker run --name nginx -d -p 80:80 nginx:latest`

### Gebruik van de database

Mysql Server

Tabellen: 
* **Item** - voor het opslaan van artikelen
* **Bron** - voor het opslaan van bronnen

### Nieuws zoeken
Het **nieuws-ophalen** script bevraagd de restservice voor bronnen en stuurt vervolgens de gevonden nieuwsartikelen terug.

`python3 nieuws-ophalen http://127.0.0.1:5000`

   
  

