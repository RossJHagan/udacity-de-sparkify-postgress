import psycopg2
from sql_queries import create_table_queries, drop_table_queries
from settings import db_host, db_create_user, db_create_pass, db_default_schema
from settings import data_store_schema, data_store_user, data_store_pass


def create_database():
    """
    - Creates and connects to the sparkifydb
    - Returns the connection and cursor to sparkifydb
    """
    
    # connect to default database
    connection_string = f"host={db_host} dbname={db_default_schema} user={db_create_user} password={db_create_pass}"
    conn = psycopg2.connect(connection_string)
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    
    # create sparkify database with UTF8 encoding
    cur.execute(f"DROP DATABASE IF EXISTS {data_store_schema}")
    cur.execute(f"CREATE DATABASE {data_store_schema} WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to default database
    conn.close()
    
    # connect to sparkify database
    sparkify_connection = f"host={db_host} dbname={data_store_schema} user={data_store_user} password={data_store_pass}"
    conn = psycopg2.connect(sparkify_connection)
    cur = conn.cursor()
    
    return cur, conn


def drop_tables(cur, conn):
    """
    Drops each table using the queries in `drop_table_queries` list.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Creates each table using the queries in `create_table_queries` list. 
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    - Drops (if exists) and Creates the sparkify database. 
    
    - Establishes connection with the sparkify database and gets
    cursor to it.  
    
    - Drops all the tables.  
    
    - Creates all tables needed. 
    
    - Finally, closes the connection. 
    """
    cur, conn = create_database()
    
    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
