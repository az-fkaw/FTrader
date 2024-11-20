-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Assets table
CREATE TABLE IF NOT EXISTS assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL UNIQUE,
    name TEXT,
    data_source TEXT,
    metadata TEXT
);

-- Trades table
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

-- Opportunities table
CREATE TABLE IF NOT EXISTS opportunities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id INTEGER NOT NULL,
    date DATE NOT NULL,
    setup TEXT,
    score TEXT,
    risk REAL,
    FOREIGN KEY(asset_id) REFERENCES assets(id)
);