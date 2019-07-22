# Project 3: Cloud Data Warehouse

### Summary
In this project, I build an ETL pipeline using AWS and Python for a hypothetical startup that has moved its growing logs of songs and user activity to the cloud.  First, the data from the cloud is loaded into staging tables, from which analytical tables are then extracted.


### ETL Process

| Staging Tables | |
| --- | --- | 
| *songs staging* | num_songs, artist_id, artist_latitude, artist_longitude, artist_location, artist_name, song_id, title, duration, year |
| *events staging* | artist, auth, firstName, gender, itemInSession, lastName, length, level, location, method, page, registration, sessionId, song, status, ts, userAgent, userId |


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

The staging tables contain largely unaltered data transferred from S3 using the `COPY` function, and in order to utilize optimized processing between S3 and Redshift I opted not to place any restrictions or conditions on the data fields being copied.

The *songs* and *artists* tables can be filled directly from the songs staging table.

The *users* table can be filled with data from the events staging table.  I sort users by descending timestamp order so as to retain the most current user information, such as paid or free level of service.

Filling *songplays* requires a join between the events and song staging tables.  The *time* table can then be filled from timestamps in the *songplays* table.


### Files

- `dwh.cfg`: contains information to access Redshift cluster and S3 bucket, and needs to be filled with the AWS Redshift host information and IAM role's ARN 
- `create_tables.py`: drops existing tables and creates new tables according to the schema
- `etl.py`: loads data into the staging tables then fills the fact and dimension tables
- `sql_queries.py`: contains all the SQL queries to create tables, stage the data from S3 using `COPY` and write to Redshift

Once `dwh.cfg` is configured with the connection info, `create_tables.py` and `etl.py` are then run sequentially.

**_Sample queries and results_**

- most popular artists

```
select a.name, count(e.artist_id) as plays
from songplays e
join artists a
on e.artist_id = a.artist_id
group by e.artist_id, a.name
order by count(e.artist_id) desc limit 5;
```

|name | plays |
|---|---|
|Dwight Yoakam	|37|
|Kid Cudi / Kanye West / Common	|10|
|Kid Cudi	|10|
|Lonnie Gordon	|9|
|Ron Carter	|9|


- most played songs

```
select a.name, s.title, count(e.song_id) as plays
from songplays e
join songs s
on e.song_id = s.song_id
join artists a
on s.artist_id = a.artist_id
group by e.song_id, a.name, s.title
order by count(e.song_id) desc limit 5;
```

|name|	title|	plays|
|---|---|---|
|Dwight Yoakam|	You're The One|	37|
|Ron Carter|	I CAN'T GET STARTED|	9|
|Lonnie Gordon|	Catch You Baby (Steve Pitron & Max Sanna Radio Edit)|	9|
|B.o.B|	Nothin' On You [feat. Bruno Mars] (Album Version)|	8|
|Usher|	Hey Daddy (Daddy's Home)|	6|
