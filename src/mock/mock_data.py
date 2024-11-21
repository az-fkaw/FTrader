import os
import sys
import json
from polygon import RESTClient

# Add 'src' to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, '..')
sys.path.append(src_path)

from db.db_utils import create_connection, hash_password

#############
# MOCK DATA #
#############
# Polygon.io API key (use environment variable)
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY", "s4aBSaSsOpGIaI6ZO2GQSFo0hSJJx3ND")
DB_PATH = "data/fTraderTest.db"

def fetch_asset_metadata(client, symbols):
    """
    Fetch metadata for assets using Polygon.io API.
    """
    metadata = []
    for symbol in symbols:
        try:
            # Fetch ticker details
            asset_info = client.get_ticker_details(symbol)
            
            # Extract relevant fields
            metadata.append({
                "symbol": symbol,
                "name": getattr(asset_info, 'name', "Unknown"),
                "data_source": "Polygon.io",
                "metadata": json.dumps({  # Serialize metadata as JSON
                    "description": getattr(asset_info, 'description', "N/A"),
                    "market": getattr(asset_info, 'market', "N/A"),
                    "primary_exchange": getattr(asset_info, 'primary_exchange', "N/A"),
                })
            })
        except Exception as e:
            print(f"Error fetching metadata for {symbol}: {e}")
    return metadata

def insert_mock_data():
    """
    Populate the test database with mock data for users, assets, trades, and opportunities.
    """
    # Connect to database
    conn = create_connection()
    cursor = conn.cursor()

    # Polygon.io client
    client = RESTClient(POLYGON_API_KEY)

    #########
    # USERS #
    #########
    mock_users = [
        {"username": "trader_joe", "password": hash_password("password123")},
        {"username": "swing_master", "password": hash_password("securepass")},
        {"username": "algo_guru", "password": hash_password("trading2024")},
    ]
    cursor.executemany("""
    INSERT INTO users (username, password_hash) VALUES (:username, :password)
    """, mock_users)
    print("Mock users inserted.")

    ##########
    # ASSETS #
    ##########
    mock_symbols = ["AAPL", "TSLA", "MSFT"]
    asset_metadata = fetch_asset_metadata(client, mock_symbols)
    cursor.executemany("""
    INSERT INTO assets (symbol, name, data_source, metadata) 
    VALUES (:symbol, :name, :data_source, :metadata)
    """, asset_metadata)
    print("Mock assets inserted.")

    ##########
    # TRADES #
    ##########
    mock_trades = [
        {
            "user_id": 1, "asset_id": 1, "entry_date": "2024-11-01", "exit_date": "2024-11-10",
            "entry_price": 150.00, "exit_price": 160.00, "setup": "Breakout", "score": "A",
            "risk": 1.0, "result": 10.0
        },
        {
            "user_id": 2, "asset_id": 2, "entry_date": "2024-10-20", "exit_date": "2024-11-05",
            "entry_price": 220.00, "exit_price": 210.00, "setup": "TrendFollowing", "score": "B",
            "risk": 0.5, "result": -5.0
        },
    ]
    cursor.executemany("""
    INSERT INTO trades (user_id, asset_id, entry_date, exit_date, entry_price, exit_price, setup, score, risk, result)
    VALUES (:user_id, :asset_id, :entry_date, :exit_date, :entry_price, :exit_price, :setup, :score, :risk, :result)
    """, mock_trades)
    print("Mock trades inserted.")

    #################
    # OPPORTUNITIES #
    #################
    mock_opportunities = [
        {"asset_id": 1, "date": "2024-11-20", "setup": "Breakout", "score": "A+", "risk": 2.0},
        {"asset_id": 2, "date": "2024-11-20", "setup": "TrendFollowing", "score": "A", "risk": 1.5},
        {"asset_id": 3, "date": "2024-11-20", "setup": "MeanReversion", "score": "B", "risk": 0.8},
    ]
    cursor.executemany("""
    INSERT INTO opportunities (asset_id, date, setup, score, risk) 
    VALUES (:asset_id, :date, :setup, :score, :risk)
    """, mock_opportunities)
    print("Mock opportunities inserted.")

    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Mock data population complete.")

if __name__ == "__main__":
    insert_mock_data()