import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """Drops tables in schema if they exist
    
    Args:
        cur, conn: cursor and connection objects to db
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """Creates new tables according to schema
    
    Args:
        cur, conn: cursor and connection objects to db
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """Parses 'dwh.cfg' for connection details to Redshift db to call drop_tables and create_tables"""
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()