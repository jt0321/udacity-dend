# Project 2: Data Modeling With Cassandra

### Summary
In this project, I document workflow and thought processes for data modeling with Apache Cassandra in a Jupyter notebook.  With a NoSQL database as Cassandra, it is important to remember that data modeling follows queries.


### Files
- `event_data`: directory containing log data in csv format to be imported into Cassandra
- `project2.ipynb`: notebook detailing the ETL process and queries creation


### Queries shaping data modeling

1. session information: give the artist, song title and song's length in the music app history that was heard during a certain session
2. user history: give the name of artist, song (sorted by itemInSession) and user (first and last name) for a specific user during a specific session
3. song's listeners: give every user name who listened to a specific song