# Project 4: Data Lake with Spark

### Summary

In this project, I build an ETL pipeline for a data lake that has evolved from a data warehouse.  I load the data from S3, process the data using Spark, and load the analytical tables back to S3.


### Data Schema and ETL Process

**Star Schema**

| Fact Table | |
| :--- | :--- |
| *songplays* | songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent |


| Dimension Tables | |
| :--- | :--- |
| *users* | user_id, first_name, last_name, gender, level |
| *songs* | song_id, title, artist_id, year, duration |
| *artists* | artist_id, name, location, latitude, longitude |
| *time* | start_time, hour, day, week, month, year, weekday |

The star schema for this analytical focus consists of a central fact table of song plays data, with dimensions along data about users, songs, artists, and timestamps.

The data has expanded so a separate directory is created to store analytical files.


### Files

- `etl.py`: creates a Spark session, connects to s3 to read data, processes the data with Spark, then writes parquet tables to s3
- `dl.cfg`: contains credentials to log into S3

Running etl.py requires access to a Spark engine.  For running Apache Spark locally I would recommend a Docker container, as detailed here https://jupyter-docker-stacks.readthedocs.io/en/latest/using/specifics.html#apache-spark.