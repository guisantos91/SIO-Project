
# Delivery 2

## Group members

- 113893 - Guilherme Santos
- 104384 - João Pinto
- 115304 - Pedro Pinto

We mantained the same structure as in the previous delivery.

## Structure
 - `client/` - contains the client side code
 - `server/` - contains the server side code
 - `views/` - contains the classes for the views

In this work, we utilised MongoDB as the primary database to manage organisational data, including documents, metadata, and user information. 


## How to run the code

Firstly, go to the `delivery2` directory.

Server:
```bash
docker compose up --build
```

Client:
```bash
python3 subject.py <command> <args>
```

Tests:
```bash
cd tests
./run_tests
```
