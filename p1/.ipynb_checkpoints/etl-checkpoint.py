import os
import glob
import psycopg2
import pandas as pd
import datetime
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Description: This function can be used to read the file in the filepath (data/song_data)
    to get the song and artist info and populate the artists and songs dim tables.

    Arguments:
        cur: the cursor object. 
        filepath: song data file path. 

    Returns:
        None
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = [str(i) for i in df.loc[0, ['song_id', 'title', 'artist_id', 'year', 'duration']].values]
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = [str(i) for i in df.loc[0, ['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values]
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Description: This function can be used to read the file in the filepath (data/log_data)
    to get the user and time info and populate the users and time dim tables.

    Arguments:
        cur: the cursor object. 
        filepath: log data file path. 

    Returns:
        None
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page']=='NextSong']

    # convert timestamp column to datetime
    t = df['ts'].apply(lambda x: datetime.datetime.fromtimestamp(x/1000))
    df['ts'] = df['ts'].apply(lambda x: str(datetime.datetime.fromtimestamp(x/1000)))
    
    # insert time data records
    time_data = ([str(ts) for ts in t], t.dt.hour, t.dt.day, t.dt.week, t.dt.month, t.dt.year, t.dt.weekday)
    column_labels = ('timestamp', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    time_df = pd.DataFrame.from_dict(dict(zip(column_labels, time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """This function applies a given func to all files in filepath, including those in subdirectories.
    
    Arguments:
        cur: cursor object
        conn: connection object
        filepath: data file path
        func: function used to parse filepath
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """Connects to sparkifydb database, and processes files in data directory"""
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()