# Ejercicio 3 - Kubernetes

Este ejercicio pretende levantar la aplicación python y una base de datos postgres con kubernetes.

## Elementos
Se ha decicido levantar los siguientes elementos en el cluster:

- Un namespace sobre el que se levantará nuestra aplicación: `datahack-ns`
- Un configMap para la configuración de la bbdd postgresql.
- Un secreto con las credenciales de la bbdd postgresql.
- Un statefulset que levante un contenedor con la bbdd postgresql. Esto ya cumple con el requisito de la persistencia. También un servicio que exponga el puerto de este contenedor a los demás elementos del cluster.
- Un deployment que levante la aplicación python. También un servicio que sirva para posteriormente exponer el puerto al exterior (por si hay varias réplicas).

## Levantar el servicio
Para levantar el servicio:

Debemos construir la imagen de docker que va a usar kubernetes `api-kubernetes:1.0.0`:
```bash
$ eval $(minikube docker-env)
$ cd 3_kubernetes/
$ docker build -t api-kubernetes:1.0.0 ../1_docker/.
```

Si no funciona por alguna razón, probar a usar la imagen de dockerhub que tengo `sergioym/api-docker:2.0.0` (Es pública)

```bash
$ cd 3_kubernetes/ # Si no estás ya en el directorio
$ kubectl apply -f namespace-config-secret.yaml # Crea namespace, configMaps y secretos necesarios
$ kubectl apply -f postgresql.yaml # Crea la bbdd postgres (statefulset para persistencia)
$ kubectl apply -f pythonapp.yaml # Crea la aplicación python (deployment)
```

Podemos evitar condiciones de carrera con un initContainer en la API, pero no se han implementado.

Con el servicio levantado, para poder realizar las pruebas, debemos hacer un `port-forward` del servicio de la API. 

```bash
$ kubectl -n datahack-ns port-forward svc/api-service 8082:5000
```

Con esto, podemos realizar las mismas pruebas:

Crear usuarios:
```bash
$ curl -X POST http://localhost:8082/user \
   -H "Content-Type: application/json" \
   -d '{"first_name": "Sergio", "last_name": "Yunta", "age": "23", "email": "sergio.yunta@example.com"}'

{"age":23,"email":"sergio.yunta@example.com","first_name":"Sergio","id":1,"last_name":"Yunta"}

$ curl -X POST http://localhost:8082/user \
   -H "Content-Type: application/json" \
   -d '{"first_name": "Usuario2", "last_name": "Apellido2", "age": "89", "email": "user2@example.com"}'
  
{"age":89,"email":"user2@example.com","first_name":"Usuario2","id":2,"last_name":"Apellido2"}
```

Vemos cuántos usuarios hay (deben ser dos):
```bash
$ curl http://localhost:8082/count

{"count":2}
```

Recuperación de usuarios:

```bash
$ curl http://localhost:8082/user/1

{"age":23,"email":"sergio.yunta@example.com","first_name":"Sergio","id":1,"last_name":"Yunta"}

$ curl http://localhost:8082/user/2

{"age":89,"email":"user2@example.com","first_name":"Usuario2","id":2,"last_name":"Apellido2"}
```

Comprobar versión:
```bash
$ curl http://localhost:8082/version

{"version":"0.0.0-SYM"}
```

## Reinicio del sistema y comprobar persistencia

Tiramos el servicio de la bbdd:
```bash
$ kubectl -n datahack-ns scale statefulset postgresql --replicas=0
$ kubectl -n datahack-ns delete deployment python
```

Levantamos el servicio de nuevo cambiando la versión de la aplicación. Si se quiere probar a cambiar la versión, cambiar el fichero `namespace-config-secret.yaml`, la variable VERSION del `ConfigMap` -> `python-config` Importante! Cambiamos la versión, pero sigue siendo la misma imagen, ya que se lee del entorno:
```bash
$ kubectl apply -f namespace-config-secret.yaml # Actualizar configmap
$ kubectl -n datahack-ns scale statefulset postgresql --replicas=1 # Volver a crear la bbdd postgres
$ kubectl apply -f pythonapp.yaml # Volver a crear la aplicación python
```

Exportar el servicio:
```bash
$ kubectl -n datahack-ns port-forward svc/api-service 8082:5000
```

Vemos que los usuarios siguen (Contador + usuarios):
```bash
$ curl http://localhost:8082/count

{"count":2}

$ curl http://localhost:8082/user/1

{"age":23,"email":"sergio.yunta@example.com","first_name":"Sergio","id":1,"last_name":"Yunta"}

$ curl http://localhost:8082/user/2

{"age":89,"email":"user2@example.com","first_name":"Usuario2","id":2,"last_name":"Apellido2"}
```

La versión ha cambiado:
```bash
$ curl http://localhost:8082/version

{"version":"0.0.1-SYM"}
```

## Escalar la solución

Podemos escalar el deployment de la API de la siguiente manera:

```bash
$ kubectl -n datahack-ns scale deployment --replicas=3 python
```

Si lo comprobamos en el dashboard, vemos como todas las réplicas han conectado y están listas para recibir peticiones.

También:
```bash
$ kubectl -n datahack-ns get pods
```

## Limpieza
```bash
$ kubectl delete -f namespace-config-secret.yaml
$ kubectl delete -f postgresql.yaml
$ kubectl delete -f pythonapp.yaml
```
