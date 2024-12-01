# Ejercicio 2 - Docker Compose

Este ejercicio pretende levantar la aplicación python y una base de datos postgres con docker compose.

## Elementos
En esta ocasión vamos a levantar los mismos elementos descritos en el apartado anterior (con docker únicamente), pero aprovechando la simplificación que nos ofrece docker compose. Tenemos que definir:

- Un servicio para la bbdd, con volumen asociado.
- Un servicio para la aplicación python.
- Un volumen mencionado previamente.

Docker compose crea automáticamente una red (network) por defecto para facilitar la comunicación entre contenedores.

## Levantar el servicio

Para levantar el servicio:

```bash
$ cd 2_docker_compose/
$ docker compose up -d 
```

Con el servicio levantado, podemos realizar las mismas pruebas:

Crear usuarios:
```bash
$ curl -X POST http://localhost:8081/user \
   -H "Content-Type: application/json" \
   -d '{"first_name": "Sergio", "last_name": "Yunta", "age": "23", "email": "sergio.yunta@example.com"}'

{"age":23,"email":"sergio.yunta@example.com","first_name":"Sergio","id":1,"last_name":"Yunta"}

$ curl -X POST http://localhost:8081/user \
   -H "Content-Type: application/json" \
   -d '{"first_name": "Usuario2", "last_name": "Apellido2", "age": "89", "email": "user2@example.com"}'
  
{"age":89,"email":"user2@example.com","first_name":"Usuario2","id":2,"last_name":"Apellido2"}
```

Vemos cuántos usuarios hay (deben ser dos):
```bash
$ curl http://localhost:8081/count

{"count":2}
```

Recuperación de usuarios:

```bash
$ curl http://localhost:8081/user/1

{"age":23,"email":"sergio.yunta@example.com","first_name":"Sergio","id":1,"last_name":"Yunta"}

$ curl http://localhost:8081/user/2

{"age":89,"email":"user2@example.com","first_name":"Usuario2","id":2,"last_name":"Apellido2"}
```

Comprobar versión:
```bash
$ curl http://localhost:8081/version

{"version":"0.0.0-SYM"}
```

## Reinicio del sistema y comprobar persistencia

Tiramos el servicio:
```bash
$ docker compose down # No borramos los datos para dejar el volumen
```

Levantamos el servicio de nuevo cambiando la versión de la aplicación. Si se quiere probar a cambiar la versión, cambiar el fichero docker compose, la variable VERSION del servicio `api-compose` Importante! Cambiamos la versión, pero sigue siendo la misma imagen, ya que se lee del entorno:
```bash
$ docker compose up -d 
```

Vemos que los usuarios siguen (Contador + usuarios):
```bash
$ curl http://localhost:8081/count

{"count":2}

$ curl http://localhost:8081/user/1

{"age":23,"email":"sergio.yunta@example.com","first_name":"Sergio","id":1,"last_name":"Yunta"}

$ curl http://localhost:8081/user/2

{"age":89,"email":"user2@example.com","first_name":"Usuario2","id":2,"last_name":"Apellido2"}
```

La versión ha cambiado:
```bash
$ curl http://localhost:8081/version

{"version":"2.1.0-SYM"}
```