# Sparkify Song Plays ETL pipeline

This pipeline receives json formatted song data and json formatted song play log events, transforming them to a
queryable data store optimised for song play analysis.

## Why

Sparkify needs to be able to analyse what songs users are listening to.  This presents the data in a format that allows
a more flexible structure in fact and dimension tables for analysis.

## Schema Design

A star schema revolving around facts and dimensions is used here to achieve a data store
that is more flexible for analysis.

The fact table `songplays` can be joined with the dimensions: `time`, `artists`, `songs`, and `users` to constrain
data for analysis.

## Querying

```sql
-- Query song titles for songs played on thanksgiving day 2018 (22nd November 2018)
SELECT songs.title AS song_title
FROM songplays JOIN songs ON songplays.song_id = songs.song_id 
WHERE songplay_timestamp >= '2018-11-22 00:00:00' AND songplay_timestamp < '2018-11-23 00:00:00';
```

## Dependencies

Python 3.7 or later.  Python 3.8.6 was used in development.

## Setup

Create and activate a local virtual environment:

`python -m venv venv`  
`source venv/bin/activate`

Install dependencies:

`pip install -r requirements.txt`

### Setup - Credentials

Environment variables are used for configuration and credentials through a `.env` file.

Create and populate credentials in a new `.env`:

`cp .env.template .env`

In the new file, remove anything after the `=` and replace with real configuration. For example:

`POSTGRES_HOST=127.0.0.1`

The `.env` file **should not** be committed.  `.gitignore` includes the `.env` to avoid this, but be mindful it may contain
credentials or configuration that could expose a security risk in a real environment when sharing code.

### Credentials - Create schema user

A user with the ability to create (and drop) a schema (db) is required under the configuration parameter
`POSTGRES_USER_CREATE_DB_PRIVILEGES` in `.env`, so that the process can automatically create the data store, and drop if
already exists on subsequent runs.

### Credentials - User to manage tables and read/write

Once the data store schema is available, privileges are dropped to the ability to create tables and read/write data into the store
under the `DATA_STORE_USER` credentials in `.env`.

The privilege to manipulate the table structures would typically be restricted even further to a distinct user,
but kept here for simplicity.

## Run

`python create_tables.py && python etl.py`