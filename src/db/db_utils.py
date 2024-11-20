##################
# DATABASE SETUP #
##################
import sqlite3
from sqlite3 import Connection

DB_PATH = "data/ftrader.db"

def create_connection() -> Connection:
    """
    Establish a connection to the SQLite database.
    Returns:
        conn (sqlite3.Connection): Connection object.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        print("Database connection established.")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        raise

def initialize_db():
    """
    Initialize the database by creating required tables.
    Tables: users, assets, trades, opportunities
    """
    conn = create_connection()
    cursor = conn.cursor()
    
    # Create tables
    with open("src/db/schema.sql", "r") as schema_file:
        schema = schema_file.read()
        cursor.executescript(schema)
        print("Database schema initialized.")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()