# django-rest

## Install project dependencies

```bash
# Install protobuf compiler
$ sudo apt-get install protobuf-compiler

# Install buildtools
$ sudo apt-get install build-essential make

# Install packages
$ pip3 install -r requirements.txt
```

## How to run

- Migrate database tables

```bash
$ cd django
$ python3 manage.py migrate
```

- Run the backend server

```bash
$ python3 manage.py runserver 0.0.0.0:8000
```

- Start the gRPC fibonacci service

```bash
$ cd gRPC
$ python3 server.py
```

- Start the gRPC and MQTT log service

```bash
$ cd mqtt
$ python3 server.py
```

## Using `curl` to perform client request

To get result of fibonacci sequence of order n. Example:

```bash
$ curl -X POST -H "Content-Type: application/json" -d '{"order" : 12}' "http://localhost:8000/rest/fibonacci"
```

To get result of pass history request. Example:

```bash
$ curl "http://localhost:8000/rest/logs"
```
