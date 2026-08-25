import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "cyber_threat_platform")

def init_database():
    print(f"Connecting to MySQL server at {DB_HOST}:{DB_PORT}...")
    # Connect without database first to create it if it doesn't exist
    try:
        engine_server = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/")
        with engine_server.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
            print(f"Database {DB_NAME} created or already exists.")
    except Exception as e:
        print(f"Failed to connect to MySQL server: {e}")
        print("Please make sure MySQL is running and credentials in .env are correct.")
        return False

    print("Connecting to database and running schema script...")
    engine_db = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    
    with open("backend/database/init_schema.sql", "r") as f:
        sql_script = f.read()
    
    # Split statements
    statements = sql_script.split(";")
    
    with engine_db.connect() as conn:
        for statement in statements:
            if statement.strip():
                try:
                    conn.execute(text(statement))
                except Exception as e:
                    print(f"Warning on executing statement: {e}")
        conn.commit()
    
    print("Schema initialized successfully.")
    
    # Insert default roles if they don't exist
    print("Inserting default roles...")
    with engine_db.connect() as conn:
        roles = ['Victim', 'Officer', 'Threat Analyst', 'Incident Responder', 'Administrator']
        for role in roles:
            try:
                conn.execute(text(f"INSERT IGNORE INTO roles (role_name) VALUES ('{role}')"))
            except Exception as e:
                pass
        conn.commit()
    print("Default roles inserted.")
    return True

if __name__ == "__main__":
    init_database()
