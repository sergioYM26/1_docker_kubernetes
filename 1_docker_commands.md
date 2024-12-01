# Ejercicio 1 - Docker

Este ejercicio pretende levantar la aplicación python y una base de datos postgres.

## Requisitos previos

Primero, mirando los requisitos necesitamos unos pasos previos:

- Una red de docker, la llamaremos `datahack-docker`
- Uno de los requisitos es la persistencia, por lo que necesitamos un volumen, crearemos uno llamado `db-data-docker`

Para la red y el volumen:
```bash
$ docker network create datahack-docker
$ docker volume create db-data-docker
```

## Construcción de la imagen

Falta construir la imagen de nuestra aplicación python:

```bash
$ cd 1_docker/
$ docker build -t api-docker:1.0.0 .
```

## Levantar la aplicación completa

Con esto, ya podemos levantar la aplicación, para ello, necesitamos primero una base de datos postgres, no se ha generado ningún dockerfile porque se puede crear el contenedor directamente desde la línea de comandos:

```bash
$ docker run -d --rm --name db-docker \
      --network datahack-docker \
      -v db-data-docker:/var/lib/postgresql/data \
      -p 5432:5432 \
      -e POSTGRES_PASSWORD=testpass \
      -e POSTGRES_USER=testuser \
      -e POSTGRES_DB=datahack \
      postgres:14
```

Una vez tengamos la bbdd levantada, podemos levantar el contenedor de la api:

```bash
$ docker run -d --rm --name api-docker \
      --network datahack-docker \
      -p 8080:5000 \
      -e DB_USER=testuser \
      -e DB_PASSWORD=testpass \
      -e DB_HOST=db-docker \
      -e DB_PORT=5432 \
      -e DB_NAME=datahack \
      -e VERSION=0.0.0-SYM \
      api-docker:1.0.0
```

Con esto, ya podemos usar nuestra API en el puerto 8080 de localhost. También la base de datos en el puerto 5432, al que nos podemos conectar con dbeaver.

Crear usuarios:
```bash
$ curl -X POST http://localhost:8080/user \
   -H "Content-Type: application/json" \
   -d '{"first_name": "Sergio", "last_name": "Yunta", "age": "23", "email": "sergio.yunta@example.com"}'

{"age":23,"email":"sergio.yunta@example.com","first_name":"Sergio","id":1,"last_name":"Yunta"}

$ curl -X POST http://localhost:8080/user \
   -H "Content-Type: application/json" \
   -d '{"first_name": "Usuario2", "last_name": "Apellido2", "age": "89", "email": "user2@example.com"}'
  
{"age":89,"email":"user2@example.com","first_name":"Usuario2","id":2,"last_name":"Apellido2"}
```

Vemos cuántos usuarios hay (deben ser dos):
```bash
$ curl http://localhost:8080/count

{"count":2}
```

Recuperación de usuarios:

```bash
$ curl http://localhost:8080/user/1

{"age":23,"email":"sergio.yunta@example.com","first_name":"Sergio","id":1,"last_name":"Yunta"}

$ curl http://localhost:8080/user/2

{"age":89,"email":"user2@example.com","first_name":"Usuario2","id":2,"last_name":"Apellido2"}
```

Comprobar versión:
```bash
$ curl http://localhost:8080/version

{"version":"0.0.0-SYM"}
```

## Reinicio del sistema y comprobar persistencia

Tiramos el servicio:
```bash
$ docker stop api-docker
$ docker stop db-docker
```

Levantamos el servicio de nuevo cambiando la versión de la aplicación. Importante! Cambiamos la versión, pero sigue siendo la misma imagen, ya que se lee del entorno:
```bash
$ docker run -d --rm --name db-docker \
      --network datahack-docker \
      -v db-data:/var/lib/postgresql/data \
      -p 5432:5432 \
      -e POSTGRES_PASSWORD=testpass \
      -e POSTGRES_USER=testuser \
      -e POSTGRES_DB=datahack \
      postgres:14

$ docker run -d --rm --name api-docker \
      --network datahack-docker \
      -p 8080:5000 \
      -e DB_USER=testuser \
      -e DB_PASSWORD=testpass \
      -e DB_HOST=db \
      -e DB_PORT=5432 \
      -e DB_NAME=datahack \
      -e VERSION=1.0.0-SYM \
      api-docker:1.0.0
```

Vemos que los usuarios siguen (Contador + usuarios):
```bash
$ curl http://localhost:8080/count

{"count":2}

$ curl http://localhost:8080/user/1

{"age":23,"email":"sergio.yunta@example.com","first_name":"Sergio","id":1,"last_name":"Yunta"}

$ curl http://localhost:8080/user/2

{"age":89,"email":"user2@example.com","first_name":"Usuario2","id":2,"last_name":"Apellido2"}
```

La versión ha cambiado:
```bash
$ curl http://localhost:8080/version

{"version":"1.0.0-SYM"}
```

## Extra: publicación de imagen en dockerhub

Para ello, debemos iniciar sesión en dockerhub, tagear la imagen y subirla
```bash
$ docker login
$ docker tag api-docker:1.0.0 sergioym/api-docker:2.0.0
$ docker push sergioym/api-docker:2.0.0
```