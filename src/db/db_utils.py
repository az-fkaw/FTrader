import sqlite3
import bcrypt
from sqlite3 import Connection

##################
# DATABASE SETUP #
##################
DB_PATH = "data/ftraderTest.db"

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
    Tables: users, assets, trades, opportunities.
    """
    conn = create_connection()
    cursor = conn.cursor()

    ###############
    # USERS TABLE #
    ###############
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    print("Table 'users' initialized.")

    ################
    # ASSETS TABLE #
    ################
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL UNIQUE,
        name TEXT,
        data_source TEXT,
        metadata TEXT
    );
    """)
    print("Table 'assets' initialized.")

    ################
    # TRADES TABLE #
    ################
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        asset_id INTEGER NOT NULL,
        entry_date DATE NOT NULL,
        exit_date DATE,
        entry_price REAL NOT NULL,
        exit_price REAL,
        setup TEXT,
        score TEXT,
        risk REAL,
        result REAL,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(asset_id) REFERENCES assets(id)
    );
    """)
    print("Table 'trades' initialized.")

    ####################### 
    # OPPORTUNITIES TABLE #
    #######################
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS opportunities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        asset_id INTEGER NOT NULL,
        date DATE NOT NULL,
        setup TEXT,
        score TEXT,
        risk REAL,
        FOREIGN KEY(asset_id) REFERENCES assets(id)
    );
    """)
    print("Table 'opportunities' initialized.")

    conn.commit()
    conn.close()
    print("Database schema created successfully.")

##################### 
# PASSWORD HANDLING #
#####################
def hash_password(password: str) -> str:
    """
    Hash a plaintext password using bcrypt.
    Args:
        password (str): The plaintext password.
    Returns:
        str: The hashed password.
    """
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a stored hash.
    Args:
        plain_password (str): The plaintext password.
        hashed_password (str): The stored password hash.
    Returns:
        bool: True if the password matches, False otherwise.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

##############
# INITIALIZE #
##############
if __name__ == "__main__":
    initialize_db()