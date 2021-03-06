import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
from settings import db_host, data_store_schema, data_store_user, data_store_pass


def process_song_file(cur, filepath):
    """Parses song data logs into songs and artists tables

    Args:
        cur: psycopg2 cursor
        filepath: string with file path relative to location the script is executed
    """
    # open song file
    df = pd.read_json(filepath, lines=True)
    df = df.where(pd.notna(df), None)

    # insert song record
    song_data = df[["song_id", "title", "artist_id", "year", "duration"]].values.tolist()[0]
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = \
        df[["artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"]].values.tolist()[0]
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """Parses event logs into time, user, and songplay tables

    handler function for processing event logs into tabular data

    Args:
        cur: psycopg2 cursor
        filepath: string with file path relative to location the script is executed
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df.page.eq('NextSong')]

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')

    # insert time data records
    time_data = (t, t.dt.hour, t.dt.day, t.dt.isocalendar().week, t.dt.month, t.dt.year, t.dt.isocalendar().day)
    column_labels = ("timestamp", "hour", "day", "week_of_year", "month", "year", "weekday")
    time_df = pd.DataFrame.from_dict(dict(zip(column_labels, time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[["userId", "firstName", "lastName", "gender", "level"]]

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

        # when no songid or artistid this data stops being meaningful for our analysis, so not inserted
        if not songid or not artistid:
            continue

        songplay_data = (
            pd.to_datetime(row.ts, unit='ms'),
            row.userId,
            row.level,
            songid,
            artistid,
            row.sessionId,
            row.location,
            row.userAgent
        )
        try:
            cur.execute(songplay_table_insert, songplay_data)
        except psycopg2.Error as e:
            print(f"Error inserting songplay: {e}")


def process_data(cur, conn, filepath, func):
    """Process log file data from json files into tables based on given processor func

    Accepts a database cursor and connection, and uses the filepath and processor `func` to
    parse the json files into the database

    Args:
        cur: psycopg2 cursor
        conn: psycopg2 connection
        filepath: string with file path relative to location the script is executed
        func: handler function accepting a cursor and filepath as arguments
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
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
    connection_string = f"host={db_host} dbname={data_store_schema} user={data_store_user} password={data_store_pass}"
    conn = psycopg2.connect(connection_string)
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
