import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Description: runs queries to copy data from S3 to db
    
    Args:
        cur, conn: cursor and connection objects to db
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    Description: runs queries to create analytical tables
    
    Arguments:
        cur, conn: cursor and connection objects to db
    
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    To be run after create_tables.py.  Runs queries in sql_queries to create staging tables and then analytical tables.
    
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()