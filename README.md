# 網路與多媒體作業

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

In 1st terminal

- Migrate database tables

```bash
$ cd django
$ python3 manage.py migrate
```

- Run the backend server

```bash
$ python3 manage.py runserver 0.0.0.0:8000
```

In 2nd terminal

- Start the fibonacci gRPC service

```bash
$ cd gRPC
$ python3 server.py
```

In 3rd terminal

- Start the Logger gRPC and MQTT log service

```bash
$ cd mqtt
$ docker run -d -it -p 1883:1883 -v $(pwd)/mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto
$ python3 server.py
```

## Using `curl` to perform client request

In 4th terminal

To get result of fibonacci sequence of order n. Example:

```bash
$ curl -X POST -H "Content-Type: application/json" -d '{"order" : 12}' "http://localhost:8000/rest/fibonacci"
```

To get result of pass history request. Example:

```bash
$ curl "http://localhost:8000/rest/logs"
```

## Video Link

- https://youtu.be/PkUJdo47Q-Q
