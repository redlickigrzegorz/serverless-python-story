Serverless Python story
=======================

General information
-------------------

The example of Python application with the usage of Serverless


Environment variables
---------------------

The set of all needed environment variables is placed in `.example.env` file.  
Set the variables in your environment manually or create your own `.env` file with all the variables inside to work with the application without any errors.

Development
-----------

Run to install all `npm` dependency packages:
```bash
$ npm install
```

Run to install all `Python` dependency packages:
```bash
$ pip install poetry
$ poetry install
```

Run to emulate `API Gateway` for processing the calls of `AWS λ` functions locally:
```bash
$ npm run offline-start
```

Run to deploy the service into the Amazon Web Services:
```bash
$ npm run deploy -- --stage STAGE_NAME
```

Run to migrate the changes into the database:
```bash
$ alembic revision --autogenerate -m "MIGRATION_DESCRIPTION"
$ alembic upgrade heads
```

Run to check the correctness of the code:
```bash
$ flake8
$ mypy .
$ pytest
```

Run to format the code:
```bash
$ black .
```
