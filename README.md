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

## Run

`python create_tables.py && python etl.py`