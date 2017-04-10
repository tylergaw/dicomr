# Dicomr

## NOTE: This project was a POC, not intended for real use. It might be helpful as Flask examples.

[https://dicomr.herokuapp.com/](https://dicomr.herokuapp.com/)

A web application for uploading and viewing DICOM images.

## Local setup

### Requirements

- Python 3.6.0
- Postgres 9.4+ _(we're using the jsonb type introduced in 9.4)_

**Soft requirements**

These are Python tools that have alternatives. These are the ones I use and I know will work well for this project
- [pyenv](https://github.com/pyenv/pyenv)
- [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)

### Create and activate a virtual env using Python 3.6.0.

```
pyenv virtualenv 3.6.0 dicomr
pyenv activate dicomr
```

### Create and set environment variables

Copy `.env.example` to `.env` and update the values for each variable for your use.

```
cp .env.example .env
```

Then export the env vars for use in the app. **Note** These env vars must be created on any system where the app is to be run.

```
source .env
```

### Create the database

In `.env` the default name is "dicomr". You can name your local db anything.
NOTE: You must have Postgres installed and configured properly. If you don't,
I recommend: [Postgres.app](https://postgresapp.com/)

```
createdb dicomr
```

### Install project requirements.

```
pip install .
```

#### A note on local file uploads

[🙃 THIS IS CURRENTLY NOT TRUE. I BROKE THIS AND JUST STARTED USING A NON-PROD S3 BUCKET FOR LOCAL UPLOADS 🙃]

During local development we don't want to upload files to S3. Instead we just
save them to a local directory that is ignored. Because it's ignored you'll
need to create it.

```
mkdir dicomr/static/uploads/tmp
```

### Run migrations

**NOTE**: Any changes made to app models in `models.py` require migrations. After making model changes create migrations with `flask db migrate`. Commit those changes.

```
flask db upgrade
```

### Run the project
```
flask run
```

Dicomr is available at [http://localhost:5000](http://localhost:5000).

## Misc developer info

### `flask clear_records`

From time to time its nice to clear out all the Record rows from the database. Both locally and in remote DBs. To make that faster there is a Flask CLI command.

```
flask clear_records
```

This is especially helpful on remote DBs. For instance running this on Heroku:

```
heroku run flask clear_records
```
