import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= """
CREATE TABLE IF NOT EXISTS staging_events
(artist VARCHAR,
 auth VARCHAR,
 firstName VARCHAR,
 gender CHAR(1),
 itemInSession INT,
 lastName VARCHAR,
 length NUMERIC,
 level VARCHAR,
 location VARCHAR,
 method VARCHAR,
 page VARCHAR,
 registration BIGINT,
 sessionId INT,
 song VARCHAR,
 status INT,
 ts BIGINT,
 userAgent VARCHAR,
 userId INT)
"""

staging_songs_table_create = """
CREATE TABLE IF NOT EXISTS staging_songs
(num_songs INT,
 artist_id VARCHAR,
 artist_latitude NUMERIC,
 artist_longitude NUMERIC,
 artist_location VARCHAR,
 artist_name VARCHAR,
 song_id VARCHAR,
 title VARCHAR,
 duration NUMERIC,
 year INT)
"""

songplay_table_create = """
CREATE TABLE IF NOT EXISTS songplays
(songplay_id INT IDENTITY(0,1) PRIMARY KEY,
 start_time TIMESTAMP,
 user_id VARCHAR,
 level VARCHAR,
 song_id VARCHAR,
 artist_id VARCHAR,
 session_id INT NOT NULL,
 location VARCHAR,
 user_agent VARCHAR
)
"""

user_table_create = """
CREATE TABLE IF NOT EXISTS users
(user_id INT PRIMARY KEY,
 first_name VARCHAR,
 last_name VARCHAR,
 gender CHAR(1),
 level VARCHAR)
"""

song_table_create = """
CREATE TABLE IF NOT EXISTS songs
(song_id VARCHAR PRIMARY KEY,
 title VARCHAR NOT NULL,
 artist_id VARCHAR NOT NULL,
 year INT,
 duration NUMERIC)
"""

artist_table_create = """
CREATE TABLE IF NOT EXISTS artists
(artist_id VARCHAR PRIMARY KEY,
 name VARCHAR NOT NULL,
 location VARCHAR,
 latitude NUMERIC,
 longitude NUMERIC)
"""

time_table_create = """
CREATE TABLE IF NOT EXISTS time
(start_time TIMESTAMP PRIMARY KEY,
 hour INT NOT NULL,
 day INT NOT NULL,
 week INT NOT NULL,
 month INT NOT NULL,
 year INT NOT NULL,
 weekday INT NOT NULL)
"""

# STAGING TABLES

staging_events_copy = """
copy staging_events from {}
credentials 'aws_iam_role={}'
format as json {}
""".format(config['S3']['LOG_DATA'], config['IAM_ROLE']['ARN'], config['S3']['LOG_JSONPATH'])

staging_songs_copy = """
copy staging_songs from {}
credentials 'aws_iam_role={}'
format as json 'auto'
""".format(config['S3']['SONG_DATA'], config['IAM_ROLE']['ARN'])

# FINAL TABLES

songplay_table_insert = """
insert into songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
(select timestamp 'epoch' + (ts/1000) * interval '1 second',
   userId, level, song_id, artist_id, sessionId, location, useragent
 from staging_events e join staging_songs s
   on e.artist like s.artist_name and e.song like s.title and e.length = s.duration
 where e.page like 'NextSong')
"""

user_table_insert = """
insert into users
(select distinct userId, firstName, lastName, gender, level from staging_events
   where userId is not null
   order by ts desc)
"""

song_table_insert = """
insert into songs
(select distinct song_id, title, artist_id, year, duration from staging_songs
 where song_id is not null)
"""

artist_table_insert = """
insert into artists 
(select distinct artist_id, artist_name, artist_location, artist_latitude, artist_longitude from staging_songs
 where artist_id is not null)
"""

time_table_insert = """
insert into time
(select start_time, extract(hour from start_time), extract(day from start_time), extract(week from start_time), 
 extract(month from start_time), extract(year from start_time), extract(dayofweek from start_time)
 from songplays)
"""

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
