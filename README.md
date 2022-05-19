# PDF Rendering Application - Rossum interview assignment

Interview assignment for Rossum - BE developer.

## Install and test

In example below I use httpie - https://httpie.io/

1) clone repository `git clone https://github.com/doubrtom/rossum-assignment`
2) go to project `cd rossum-assignment`
3) create `.env` file `make create-testing-env`
4) build docker images `docker-compose build`
5) run services `docker-compose up -d`
6) send request `http --form http://127.0.0.1:5001/rendering-pdf pdf_file@YOUR_FILE.pdf`


## Run tests in docker

Tests are written in `pytest` and can be found in `tests` folder.

1) `docker-compose up -d`
2) `docker-compose run pdf_renderer_api pipenv run make test`


## OpenAPI documentation

Documentation can be found:

- OpenApi schema: http://localhost:5001/apispec_1.json
- Swagger UI: http://localhost:5001/apidocs/

You have to start up application to see documentation.


## Project structure

- `pdf_renderer`: All application code
- `data`: Folder to save generated data, this folder is mounted as docker volume.
  It can be mounted to any high-speed device for better performance in production.
- `pg-init-scripts`: Init scripts for PostgresSQL DB, when docker is initialising DB volume.
- `scripts`: Entry points (scripts) for Docker API service and Worker service.
- `tests`: Folder with unit/functional tests.
- `Makefile`: Makefile with handy command during development
