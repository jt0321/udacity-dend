# Project 1: Data Modeling With Postgres

### Summary
In this project, I apply what I've learned on data modeling with Postgres and build an ETL pipeline using Python for a hypothetical startup that is interested in its songs and user activity.  The star schema for this analytical focus consists of a central fact table of song plays data, with dimensions along data about users, songs, artists, and timestamps.  The ETL pipeline, written in Python, implements this star schema by converting information from JSON files to a Postgres database.


### Star Schema and ETL Process

| Fact Table | |
| :--- | :--- |
| **songplays** | *songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent* |


| Dimension Tables | |
| :--- | :--- |
| **users** | *user_id, first_name, last_name, gender, level* |
| **songs** | *song_id, title, artist_id, year, duration* |
| **artists** | *artist_id, name, location, latitude, longitude* |
| **time** | *start_time, hour, day, week, month, year, weekday* |

The **songs** and **artists** tables are filled by data from the `song_data` directory.  The **users** and **time** tables are filled by data from the `log_data` directory.  The **songplays** table is filled by linking information from both `log_data` and `song_data`.

### Files
The files to create the database should be run in order as follows using python, e.g. `python filename.py`
- `create_tables.py`: drops tables if any remain in the database and creates new tables based on the schema defined
- `etl.py`: reads the files in the `data` directory and inserts data defined by the previous file

An essential file imported by both is
- `sql_queries.py`: contains predefined queries for use with Postgres SQL

The Jupyter notebooks facilitate creation of the ETL pipeline as well as testing SQL queries.

### Sample Queries and Expected Results

> `%SQL SELECT count(*) FROM songplays WHERE user_id = '73';`

**output**: count 289

> `%SQL SELECT * FROM users LIMIT 5;`

**output**: 

| user_id | first_name | last_name | gender | level |
| :--- | :--- | :--- | :--- | :--- |
| 73	| Jacob	| Klein	| M	| paid
| 24	| Layla	| Griffin	| F	| paid
| 50	| Ava	| Robinson	| F	| free
| 54	| Kaleb	| Cook	| M	| free
| 32	| Lily	| Burns	| F	| free


