import os
import psycopg2
from flask import Flask, request, render_template
from dotenv import load_dotenv

# Load secrets from your .env file
load_dotenv()

app = Flask(__name__)

def get_db_connection():
    """Opens a direct raw SQL connection to PostgreSQL using environment variables."""
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST', 'localhost')
    )
    return conn

def init_db():
    """Automatically creates the users table on startup if it doesn't exist."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(80) UNIQUE NOT NULL,
            password_hash VARCHAR(200) NOT NULL
        );
    """)
    
    conn.commit()
    cur.close()
    conn.close()

# Initialize the database table when the app boots up
init_db()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if path == '':
        return render_template('index.html')
    
    # This handles any incoming request routed through your Cloudflare tunnel[cite: 2]
    print(f"Received request for path: /{path}")
    return "Hello from your Ubuntu home server! Cloudflare tunnel is connected.", 200

if __name__ == '__main__':
    # Runs on port 5000 locally; your cloudflared tunnel config will point to this port[cite: 2]
    app.run(host='0.0.0.0', port=5000)
